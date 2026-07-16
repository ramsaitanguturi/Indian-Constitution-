import os
import sys
import json

# Add backend directory to sys.path to allow absolute imports of app
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.db.chroma import db_manager
from app.core.logging import setup_logging, logger

setup_logging()

def reset_collections():
    """
    Resets the collections in ChromaDB to ensure clean data ingestion.
    """
    logger.info("Resetting ChromaDB collections...")
    for name in ["constitution_parents", "constitution_children", "case_laws"]:
        try:
            db_manager.client.delete_collection(name)
            logger.info(f"Deleted existing collection: {name}")
        except Exception:
            # Collection didn't exist, which is fine
            pass

def ingest_constitution():
    """
    Ingests parent articles and child chunks.
    """
    raw_path = os.path.join(backend_dir, "data", "raw", "constitution_articles.json")
    if not os.path.exists(raw_path):
        logger.error(f"Raw constitution articles not found at {raw_path}")
        return

    with open(raw_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    parents_col = db_manager.get_parents_collection()
    children_col = db_manager.get_children_collection()

    parent_ids = []
    parent_docs = []
    parent_metadatas = []

    child_ids = []
    child_docs = []
    child_metadatas = []

    for art in articles:
        art_num = art["article_number"]
        parent_id = f"art_{art_num}"

        # Parent details
        parent_ids.append(parent_id)
        parent_docs.append(art["full_text"])
        parent_metadatas.append({
            "article_number": art_num,
            "title": art["title"],
            "part": art["part"],
            "chapter": art.get("chapter", "") or "",
            "type": "parent",
            "fundamental_right": art.get("fundamental_right", ""),
            "constitutional_part": art.get("constitutional_part", ""),
            "related_articles": ",".join(art.get("related_articles", []))
        })

        # Child clauses details
        for idx, clause in enumerate(art.get("clauses", [])):
            c_id = clause.get("clause_id", f"{parent_id}_child_{idx}")
            child_ids.append(c_id)
            child_docs.append(clause["text"])
            child_metadatas.append({
                "parent_id": parent_id,
                "article_number": art_num,
                "clause": clause.get("clause", ""),
                "category": clause["category"],
                "type": "child",
                "keywords": ",".join(clause.get("keywords", [])),
                "legal_topics": ",".join(clause.get("legal_topics", [])),
                "related_cases": ",".join(clause.get("related_cases", [])),
                "title": art["title"],
                "part": art["part"],
                "chapter": art.get("chapter", "") or "",
                "related_articles": ",".join(art.get("related_articles", []))
            })

    # Add to ChromaDB
    if parent_ids:
        logger.info(f"Ingesting {len(parent_ids)} parent articles into 'constitution_parents'...")
        parents_col.add(ids=parent_ids, documents=parent_docs, metadatas=parent_metadatas)

    if child_ids:
        logger.info(f"Ingesting {len(child_ids)} child chunks into 'constitution_children'...")
        children_col.add(ids=child_ids, documents=child_docs, metadatas=child_metadatas)

def ingest_cases():
    """
    Ingests landmark cases.
    """
    raw_path = os.path.join(backend_dir, "data", "raw", "landmark_cases.json")
    if not os.path.exists(raw_path):
        logger.error(f"Raw landmark cases not found at {raw_path}")
        return

    with open(raw_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    cases_col = db_manager.get_cases_collection()

    case_ids = []
    case_docs = []
    case_metadatas = []

    for case in cases:
        case_ids.append(case["id"])
        
        # Build a detailed text representation for similarity search
        facts = case.get("facts", "")
        issues = case.get("legal_issue") or case.get("issues", "")
        judgment = case.get("judgment", "")
        principle = case.get("legal_principle", "")
        ratio = case.get("ratio_decidendi") or case.get("ratio", "")
        keywords_str = ",".join(case.get("keywords", [])) if isinstance(case.get("keywords"), list) else case.get("keywords", "")
        
        doc_text = f"Case: {case['case_name']}\nFacts: {facts}\nLegal Issue: {issues}\nJudgment: {judgment}\nLegal Principle: {principle}\nRatio Decidendi: {ratio}\nKeywords: {keywords_str}"
        case_docs.append(doc_text)
        
        case_metadatas.append({
            "case_name": case["case_name"],
            "citation": case.get("citation", ""),
            "year": case["year"],
            "court": case.get("court", "Supreme Court of India"),
            "category": case.get("category", ""),
            # Chroma DB metadata does not support lists directly, so join as comma-separated string
            "articles_cited": ",".join(case.get("articles_involved", [])),
            "ratio": ratio,
            "legal_principle": principle,
            "keywords": keywords_str
        })

    if case_ids:
        logger.info(f"Ingesting {len(case_ids)} landmark cases into 'case_laws'...")
        cases_col.add(ids=case_ids, documents=case_docs, metadatas=case_metadatas)

def main():
    try:
        reset_collections()
        ingest_constitution()
        ingest_cases()
        logger.info("Ingestion completed successfully!")
        if db_manager._client:
            logger.info("Closing database client to flush changes to disk...")
            db_manager._client.close()
    except Exception as e:
        logger.exception(f"An error occurred during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
