import time
from typing import List, Dict, Any, Optional
from fastapi import UploadFile
from ..utils.file_utils import save_temp_file, cleanup_temp_file, validate_file, validate_file_size
from ..models.cv_model import CVData, CVSummary, CVResponse
from ..models.analysis_model import AnalysisLog
from .ocr_service import ocr_service
from .llm_service import llm_service
from .storage_service import storage_service

class AnalysisService:
    def __init__(self):
        self.ocr = ocr_service
        self.llm = llm_service
        self.storage = storage_service
    
    async def analyze_cvs(self, files: List[UploadFile], query: Optional[str] = None) -> CVResponse:
        """Analisa CVs e retorna resultado baseado na query"""
        start_time = time.time()
        analysis_id = self.storage.create_analysis_id()
        
        for file in files:
            if not validate_file(file):
                raise ValueError(f"Tipo de arquivo não suportado: {file.content_type}")
            if not validate_file_size(file):
                raise ValueError(f"Arquivo muito grande: {file.filename}")
        
        temp_files = {}
        cv_summaries = []
        
        try:
            for file in files:
                temp_path = await save_temp_file(file)
                temp_files[file.filename] = temp_path
            
            extracted_texts = self.ocr.process_multiple_files(temp_files)
            
            for filename, text in extracted_texts.items():
                if not text.startswith("Erro"):
                    summary = self.llm.generate_cv_summary(text, filename)
                    cv_summaries.append(summary)
            
            if query and cv_summaries:
                if len(cv_summaries) > 1 and any(word in query.lower() for word in ["compar", "melhor", "ranking", "versus"]):

                    analysis_type = "comparison"
                    result = self.llm.compare_candidates(cv_summaries, query)
                else:

                    analysis_type = "query"
                    result = {
                        "answer": self.llm.answer_query(cv_summaries, query),
                        "summaries": [summary.dict() for summary in cv_summaries]
                    }
            else:

                analysis_type = "summary"
                result = {
                    "summaries": [summary.dict() for summary in cv_summaries],
                    "total_candidates": len(cv_summaries)
                }
            
            processing_time = time.time() - start_time
            

            response = CVResponse(
                analysis_id=analysis_id,
                analysis_type=analysis_type,
                result=result,
                processed_files=[file.filename for file in files],
                query=query
            )
            

            log = AnalysisLog(
                analysis_id=analysis_id,
                files_processed=[file.filename for file in files],
                query=query,
                analysis_type=analysis_type,
                result=result,
                processing_time=processing_time
            )
            self.storage.save_analysis_log(log)
            
            return response
            
        except Exception as e:
            raise Exception(f"Erro durante análise: {str(e)}")
        
        finally:
            # Limpa arquivos temporários
            for temp_path in temp_files.values():
                cleanup_temp_file(temp_path)
    
    def get_analysis_history(self, limit: int = 10) -> List[AnalysisLog]:
        """Recupera histórico de análises"""
        return self.storage.get_recent_analyses(limit)
    
    def get_analysis_by_id(self, analysis_id: str) -> Optional[AnalysisLog]:
        """Recupera análise específica por ID"""
        return self.storage.get_analysis_log(analysis_id)

analysis_service = AnalysisService()
