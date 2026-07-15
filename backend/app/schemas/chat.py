from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str = Field(..., description="The legal scenario or question from the user")
    limit: Optional[int] = Field(5, description="Number of results to retrieve")

class ArticleResponse(BaseModel):
    article_number: str = Field(..., description="Article number")
    title: str = Field(..., description="Article title")
    clause: Optional[str] = Field(None, description="Matched clause detail (e.g., '19(1)(a)')")
    content: str = Field(..., description="Content of the matched clause or parent article")
    source_document: str = Field(..., description="Source document identifier (e.g., 'Constitution of India')")
    related_cases: List[str] = Field(default=[], description="Related landmark cases")
    similarity_score: float = Field(..., description="Calculated similarity or fusion score")

class CaseResponse(BaseModel):
    case_name: str = Field(..., description="Case name")
    citation: str = Field(..., description="Case citation")
    summary: str = Field(..., description="Detailed summary of the case")
    similarity_score: float = Field(..., description="Calculated similarity score")

class ValidationResponse(BaseModel):
    is_valid: Optional[bool] = Field(None, description="Whether the response is verified as valid and accurate")
    hallucination_risk: Optional[str] = Field(None, description="Risk level of hallucination (High, Medium, Low)")
    details: Optional[str] = Field(None, description="Verification details or checks performed")
    action: Optional[str] = Field(None, description="Workflow action decision (proceed or stop)")
    category: Optional[str] = Field(None, description="Detected legal category")
    issue: Optional[str] = Field(None, description="Detected legal issue description")

class QueryResponse(BaseModel):
    question: str = Field(..., description="The original query")
    articles: List[ArticleResponse] = Field(default=[], description="List of retrieved relevant constitutional articles")
    cases: List[CaseResponse] = Field(default=[], description="List of retrieved relevant landmark cases")
    reasoning: Optional[str] = Field(None, description="Legal reasoning connecting cases and articles")
    verdict: Optional[str] = Field(None, description="Predicted legal verdict")
    confidence: Optional[str] = Field(None, description="Confidence score or level (e.g. 'High', 'Medium', 'Low')")
    validation_result: Optional[ValidationResponse] = Field(None, description="Validation metrics from the router and validator agents")

