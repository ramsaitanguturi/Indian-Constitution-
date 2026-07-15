from pydantic import BaseModel, Field
from typing import List, Optional

class ParentDocument(BaseModel):
    id: str = Field(..., description="Unique article ID (e.g., 'art_21')")
    article_number: str = Field(..., description="Constitutional article number (e.g., '21')")
    title: str = Field(..., description="Title of the article")
    part: str = Field(..., description="Part of the Constitution (e.g., 'Part III')")
    full_text: str = Field(..., description="Full original text of the constitutional article")
    fundamental_right: str = Field(..., description="Name of the fundamental right category (e.g., 'Right to Freedom')")
    constitutional_part: str = Field(..., description="Constitutional Part identifier (e.g., 'Part III')")
    related_articles: List[str] = Field(default=[], description="List of related articles (e.g., ['19', '20'])")

class ChildChunk(BaseModel):
    id: str = Field(..., description="Unique child ID (e.g., 'art_21_child_0')")
    parent_id: str = Field(..., description="Matches the ID of the parent article")
    article_number: str = Field(..., description="Article number")
    clause: Optional[str] = Field(None, description="Clause label (e.g., '19(1)(a)')")
    text: str = Field(..., description="Segment of clause text or annotations")
    category: str = Field(..., description="Topic label (e.g., 'Privacy', 'Speech')")
    keywords: List[str] = Field(default=[], description="Keywords for indexing")
    legal_topics: List[str] = Field(default=[], description="Key legal topics/principles covered")
    related_cases: List[str] = Field(default=[], description="Key landmark cases related to this clause")

class CaseLaw(BaseModel):
    id: str = Field(..., description="Unique case ID (e.g., 'case_puttaswamy_2017')")
    case_name: str = Field(..., description="Name of the case (e.g., 'Justice K.S. Puttaswamy v. Union of India')")
    citation: str = Field(..., description="Case citation (e.g., 'AIR 2017 SC 4161')")
    year: int = Field(..., description="Year of judgment")
    articles_cited: List[str] = Field(..., description="List of constitutional articles cited")
    ratio: str = Field(..., description="Ratio decidendi of the case")
    summary: str = Field(..., description="Detailed summary of the judgment and facts")
