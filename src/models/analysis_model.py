from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AnalysisLog(BaseModel):
    analysis_id: str
    files_processed: List[str]
    query: Optional[str]
    analysis_type: str
    result: Dict[str, Any]
    processing_time: float
    timestamp: datetime = datetime.now()
    
class ComparisonResult(BaseModel):
    candidate_rankings: List[Dict[str, Any]]
    comparison_criteria: List[str]
    summary: str
    
class SummaryResult(BaseModel):
    summaries: Dict[str, str]
    key_insights: List[str]
    overall_analysis: str