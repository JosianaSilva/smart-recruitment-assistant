from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CVData(BaseModel):
    filename: str
    extracted_text: str
    file_type: str
    processed_at: datetime = datetime.now()
    
class CVSummary(BaseModel):
    filename: str
    summary: str
    key_skills: List[str]
    experience_years: Optional[float]
    education: Optional[str]
    contact_info: Dict[str, Any]
    
class CVAnalysisRequest(BaseModel):
    query: Optional[str] = None
    comparison_type: Optional[str] = "summary"  # "summary" ou "comparison"
    
class CVResponse(BaseModel):
    analysis_id: str
    analysis_type: str
    result: Dict[str, Any]
    processed_files: List[str]
    query: Optional[str]
    timestamp: datetime = datetime.now()