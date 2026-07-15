from typing import List, Dict, Any, Tuple
import math
import re
from app.db.chroma import db_manager
from app.core.logging import logger
from app.schemas.chat import ArticleResponse, CaseResponse, QueryResponse
from app.services.preprocessor import query_preprocessor

class BM25:
    def __init__(self, documents: List[str], ids: List[str], metadatas: List[Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.documents = documents
        self.ids = ids
        self.metadatas = metadatas
        self.k1 = k1
        self.b = b
        self.doc_len = []
        self.avg_doc_len = 0.0
        self.doc_freqs = []
        self.idf = {}
        self.nd = len(documents)
        self._initialize()

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.split()

    def _initialize(self):
        df = {}
        total_len = 0
        for doc in self.documents:
            tokens = self._tokenize(doc)
            self.doc_len.append(len(tokens))
            total_len += len(tokens)
            
            # Word frequencies in this document
            freqs = {}
            for t in tokens:
                freqs[t] = freqs.get(t, 0) + 1
            self.doc_freqs.append(freqs)
            
            # Update document frequency for IDF
            for t in set(tokens):
                df[t] = df.get(t, 0) + 1
                
        self.avg_doc_len = total_len / self.nd if self.nd > 0 else 0
        
        # Calculate IDF (BM25 version)
        for word, freq in df.items():
            self.idf[word] = math.log((self.nd - freq + 0.5) / (freq + 0.5) + 1.0)

    def score(self, query: str) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        scored_docs = []
        for i in range(self.nd):
            score = 0.0
            doc_len = self.doc_len[i]
            freqs = self.doc_freqs[i]
            for token in query_tokens:
                if token in freqs:
                    tf = freqs[token]
                    idf = self.idf.get(token, 0.0)
                    numerator = tf * (self.k1 + 1.0)
                    denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                    score += idf * (numerator / denominator)
            scored_docs.append({
                "id": self.ids[i],
                "document": self.documents[i],
                "metadata": self.metadatas[i],
                "score": score
            })
        # Sort by score descending
        return sorted(scored_docs, key=lambda x: x["score"], reverse=True)

class RAGService:
    def __init__(self):
        self.parents_col = db_manager.get_parents_collection()
        self.children_col = db_manager.get_children_collection()
        self.cases_col = db_manager.get_cases_collection()
        self._bm25_initialized = False
        self.bm25_children = None
        self.bm25_cases = None

    def _ensure_bm25_indices(self):
        """
        Lazily builds the in-memory BM25 indices from the ChromaDB collection contents.
        """
        if self._bm25_initialized:
            return
        
        logger.info("Initializing in-memory BM25 indices from ChromaDB...")
        
        # Load children collection for BM25
        try:
            children = self.children_col.get()
            if children and "ids" in children and children["ids"]:
                self.bm25_children = BM25(
                    documents=children["documents"],
                    ids=children["ids"],
                    metadatas=children["metadatas"]
                )
                logger.info(f"Successfully built BM25 index for {len(children['ids'])} child chunks.")
            else:
                logger.warning("No child chunks found in ChromaDB. BM25 child index is empty.")
                self.bm25_children = None
        except Exception as e:
            logger.exception(f"Error loading children BM25 index: {e}")
            self.bm25_children = None

        # Load cases collection for BM25
        try:
            cases = self.cases_col.get()
            if cases and "ids" in cases and cases["ids"]:
                self.bm25_cases = BM25(
                    documents=cases["documents"],
                    ids=cases["ids"],
                    metadatas=cases["metadatas"]
                )
                logger.info(f"Successfully built BM25 index for {len(cases['ids'])} landmark cases.")
            else:
                logger.warning("No cases found in ChromaDB. BM25 cases index is empty.")
                self.bm25_cases = None
        except Exception as e:
            logger.exception(f"Error loading cases BM25 index: {e}")
            self.bm25_cases = None

        self._bm25_initialized = True

    def reset_bm25_indices(self):
        """
        Forces rebuild of BM25 indices on next query.
        """
        self._bm25_initialized = False

    def retrieve_articles(self, query_text: str, limit: int = 3, processed_query: Dict[str, Any] = None) -> List[ArticleResponse]:
        """
        Retrieves relevant constitutional articles using child-first hierarchical hybrid RAG.
        """
        if not processed_query:
            processed_query = query_preprocessor.preprocess(query_text)
        
        cleaned_query = processed_query["cleaned_query"]
        extracted_keywords = processed_query["keywords"]
        search_query = processed_query["search_query"]
        
        # Ensure BM25 indices are active
        self._ensure_bm25_indices()
        
        # 2. Hybrid Retrieval on Child Chunks
        # A. Semantic search
        semantic_child_results = self.children_col.query(
            query_texts=[search_query],
            n_results=min(limit * 4, 30)
        )
        
        semantic_child_ids = []
        semantic_child_map = {}
        if semantic_child_results and semantic_child_results["ids"] and len(semantic_child_results["ids"][0]) > 0:
            semantic_child_ids = semantic_child_results["ids"][0]
            for idx, doc_id in enumerate(semantic_child_ids):
                semantic_child_map[doc_id] = {
                    "document": semantic_child_results["documents"][0][idx],
                    "metadata": semantic_child_results["metadatas"][0][idx],
                    "distance": semantic_child_results["distances"][0][idx] if "distances" in semantic_child_results and semantic_child_results["distances"] else None
                }

        # B. Keyword search (BM25)
        bm25_child_results = []
        if self.bm25_children:
            bm25_child_results = self.bm25_children.score(search_query)
            
        bm25_child_ids = [res["id"] for res in bm25_child_results[:min(limit * 4, 30)]]
        bm25_child_map = {res["id"]: res for res in bm25_child_results}

        # 3. Reciprocal Rank Fusion (RRF) for Child Chunks
        k_rrf = 60
        rrf_scores = {}
        for rank, doc_id in enumerate(semantic_child_ids, 1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k_rrf + rank)
            
        for rank, doc_id in enumerate(bm25_child_ids, 1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k_rrf + rank)
            
        fused_child_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

        # 4. Metadata Keyword Overlap Reranking
        children_lookup = {}
        for doc_id in rrf_scores.keys():
            if doc_id in semantic_child_map:
                children_lookup[doc_id] = semantic_child_map[doc_id]
            elif doc_id in bm25_child_map:
                children_lookup[doc_id] = {
                    "document": bm25_child_map[doc_id]["document"],
                    "metadata": bm25_child_map[doc_id]["metadata"]
                }
                
        reranked_results = []
        for doc_id in fused_child_ids:
            rrf_score = rrf_scores[doc_id]
            doc_data = children_lookup[doc_id]
            metadata = doc_data["metadata"]
            
            # Extract keywords and legal topics lists
            keywords_str = metadata.get("keywords", "")
            topics_str = metadata.get("legal_topics", "")
            
            keywords_list = [k.strip().lower() for k in keywords_str.split(",") if k.strip()]
            topics_list = [t.strip().lower() for t in topics_str.split(",") if t.strip()]
            
            # Count overlaps
            overlap_count = 0
            for kw in extracted_keywords:
                kw_lower = kw.lower()
                if kw_lower in keywords_list:
                    overlap_count += 2  # Keyword match gets higher priority
                if kw_lower in topics_list:
                    overlap_count += 1
            
            # Apply boost
            boost = 1.0 + (0.2 * overlap_count)
            boosted_score = rrf_score * boost
            
            reranked_results.append({
                "id": doc_id,
                "document": doc_data["document"],
                "metadata": metadata,
                "rrf_score": rrf_score,
                "final_score": boosted_score
            })
            
        # Re-sort based on boosted final score
        reranked_results = sorted(reranked_results, key=lambda x: x["final_score"], reverse=True)
        top_children = reranked_results[:limit]
        
        # 5. Fetch Parent Articles and Reconstruct Response
        parent_ids = list(set([child["metadata"]["parent_id"] for child in top_children if child["metadata"].get("parent_id")]))
        
        parents_map = {}
        if parent_ids:
            parents_data = self.parents_col.get(ids=parent_ids)
            if parents_data and "ids" in parents_data:
                for i, p_id in enumerate(parents_data["ids"]):
                    parents_map[p_id] = {
                        "document": parents_data["documents"][i],
                        "metadata": parents_data["metadatas"][i]
                    }

        # Build ArticleResponses
        max_rrf_possible = 2.0 / 61.0
        retrieved_articles = []
        
        for child in top_children:
            meta = child["metadata"]
            p_id = meta.get("parent_id")
            parent_info = parents_map.get(p_id)
            
            # Retrieve parent metadata if available
            parent_title = "Constitution Provision"
            if parent_info:
                parent_title = parent_info["metadata"].get("title", parent_title)
            
            # Parse list fields back from string
            related_cases_str = meta.get("related_cases", "")
            related_cases = [c.strip() for c in related_cases_str.split(",") if c.strip()]
            
            # Normalize the score (clip at 1.0)
            norm_score = min(round(child["final_score"] / max_rrf_possible, 4), 1.0)
            
            retrieved_articles.append(ArticleResponse(
                article_number=meta.get("article_number", ""),
                title=parent_title,
                clause=meta.get("clause"),
                content=child["document"],  # Specific clause content
                source_document="Constitution of India",
                related_cases=related_cases,
                similarity_score=norm_score
            ))
            
        return retrieved_articles

    def retrieve_cases(self, query_text: str, retrieved_articles: List[ArticleResponse], limit: int = 3, processed_query: Dict[str, Any] = None) -> List[CaseResponse]:
        """
        Retrieves relevant landmark cases, boosting those citing retrieved articles.
        """
        if not processed_query:
            processed_query = query_preprocessor.preprocess(query_text)
            
        search_query = processed_query["search_query"]
        
        # Ensure BM25 indices are active
        self._ensure_bm25_indices()
        
        # A. Semantic Search on Case Laws
        semantic_case_results = self.cases_col.query(
            query_texts=[search_query],
            n_results=min(limit * 3, 10)
        )
        
        semantic_case_ids = []
        semantic_case_map = {}
        if semantic_case_results and semantic_case_results["ids"] and len(semantic_case_results["ids"][0]) > 0:
            semantic_case_ids = semantic_case_results["ids"][0]
            for idx, case_id in enumerate(semantic_case_ids):
                semantic_case_map[case_id] = {
                    "document": semantic_case_results["documents"][0][idx],
                    "metadata": semantic_case_results["metadatas"][0][idx]
                }

        # B. Keyword Search on Case Laws (BM25)
        bm25_case_results = []
        if self.bm25_cases:
            bm25_case_results = self.bm25_cases.score(search_query)
            
        bm25_case_ids = [res["id"] for res in bm25_case_results[:min(limit * 3, 10)]]
        bm25_case_map = {res["id"]: res for res in bm25_case_results}

        # C. Fuse Case Results (RRF)
        k_rrf = 60
        case_rrf_scores = {}
        for rank, case_id in enumerate(semantic_case_ids, 1):
            case_rrf_scores[case_id] = case_rrf_scores.get(case_id, 0.0) + 1.0 / (k_rrf + rank)
            
        for rank, case_id in enumerate(bm25_case_ids, 1):
            case_rrf_scores[case_id] = case_rrf_scores.get(case_id, 0.0) + 1.0 / (k_rrf + rank)
            
        fused_case_ids = sorted(case_rrf_scores.keys(), key=lambda x: case_rrf_scores[x], reverse=True)

        # D. Boost cases that explicitly cite any of the retrieved parent article numbers
        retrieved_article_nums = set([art.article_number for art in retrieved_articles])
        
        cases_lookup = {}
        for c_id in case_rrf_scores.keys():
            if c_id in semantic_case_map:
                cases_lookup[c_id] = semantic_case_map[c_id]
            elif c_id in bm25_case_map:
                cases_lookup[c_id] = {
                    "document": bm25_case_map[c_id]["document"],
                    "metadata": bm25_case_map[c_id]["metadata"]
                }

        reranked_cases = []
        for case_id in fused_case_ids:
            rrf_score = case_rrf_scores[case_id]
            case_data = cases_lookup[case_id]
            metadata = case_data["metadata"]
            
            # Extract cited articles
            cited_articles_str = metadata.get("articles_cited", "")
            cited_numbers = re.findall(r'\b\d+\b', cited_articles_str)
            
            # Check overlap
            cited_overlap = False
            for num in cited_numbers:
                if num in retrieved_article_nums:
                    cited_overlap = True
                    break
            
            # Apply boost if there is overlap (+50% score boost)
            boost = 1.5 if cited_overlap else 1.0
            final_score = rrf_score * boost
            
            reranked_cases.append({
                "id": case_id,
                "document": case_data["document"],
                "metadata": metadata,
                "final_score": final_score
            })

        # Re-sort and take top limits
        reranked_cases = sorted(reranked_cases, key=lambda x: x["final_score"], reverse=True)
        top_cases = reranked_cases[:limit]
        
        # Build CaseResponses
        max_rrf_possible = 2.0 / 61.0
        retrieved_cases = []
        for case in top_cases:
            meta = case["metadata"]
            norm_score = min(round(case["final_score"] / max_rrf_possible, 4), 1.0)
            
            retrieved_cases.append(CaseResponse(
                case_name=meta.get("case_name", ""),
                citation=meta.get("citation", ""),
                summary=case["document"],
                similarity_score=norm_score
            ))
            
        return retrieved_cases

    def query(self, query_text: str, limit: int = 3) -> QueryResponse:
        """
        Executes Advanced Phase 2 Hierarchical Hybrid RAG.
        """
        logger.info(f"Processing query in Phase 2 RAG Service: '{query_text}'")
        
        # 1. Query preprocessing
        processed_query = query_preprocessor.preprocess(query_text)
        
        # 2. Retrieve articles
        retrieved_articles = self.retrieve_articles(query_text, limit=limit, processed_query=processed_query)
        
        # 3. Retrieve cases
        retrieved_cases = self.retrieve_cases(query_text, retrieved_articles=retrieved_articles, limit=limit, processed_query=processed_query)
        
        # 4. Generate reasoning & verdict fallback
        reasoning = None
        verdict = None
        confidence = None

        if retrieved_articles:
            best_art = retrieved_articles[0]
            best_case = retrieved_cases[0] if retrieved_cases else None
            
            reasoning = (
                f"The scenario falls under the scope of Article {best_art.article_number} ({best_art.title}), "
                f"specifically referencing clause {best_art.clause}. "
                f"This provision guarantees protected rights (e.g., category: {best_art.clause})."
            )
            if best_case:
                reasoning += f" Related landmark jurisprudence includes {best_case.case_name} ({best_case.citation}), which establishes that these protections must be strictly enforced against arbitrary state actions."
            
            verdict = f"State or government actions violating the criteria set under Article {best_art.article_number} may be declared unconstitutional."
            confidence = "High"
            if len(retrieved_articles) > 1 and retrieved_articles[0].similarity_score < 0.5:
                confidence = "Medium"

        return QueryResponse(
            question=query_text,
            articles=retrieved_articles,
            cases=retrieved_cases,
            reasoning=reasoning,
            verdict=verdict,
            confidence=confidence
        )


rag_service = RAGService()
