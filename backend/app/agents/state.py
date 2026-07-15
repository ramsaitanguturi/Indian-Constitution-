from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    user_query: str
    processed_query: Dict[str, Any]
    detected_legal_issue: str
    retrieved_articles: List[Dict[str, Any]]
    retrieved_cases: List[Dict[str, Any]]
    reasoning_chain: str
    validation_result: Dict[str, Any]
    confidence_score: float
    final_answer: str
    verdict: Optional[str]

