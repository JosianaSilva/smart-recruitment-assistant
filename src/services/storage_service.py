from pymongo import MongoClient
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from ..utils.config import config
from ..models.analysis_model import AnalysisLog

class StorageService:
    def __init__(self):
        try:
            self.client = MongoClient(config.MONGODB_URL)
            self.db = self.client[config.DATABASE_NAME]
            self.analysis_collection = self.db.analysis_logs

            self.client.server_info()
        except Exception as e:
            print(f"Aviso: MongoDB não disponível: {e}")
            self.client = None
            self.db = None
            self.analysis_collection = None
    
    def save_analysis_log(self, log: AnalysisLog) -> str:
        """Salva log de análise no MongoDB"""
        if not self.analysis_collection:
            print("MongoDB não disponível - log não salvo")
            return log.analysis_id
        
        try:
            log_dict = log.dict()
            self.analysis_collection.insert_one(log_dict)
            return log.analysis_id
        except Exception as e:
            print(f"Erro ao salvar log: {e}")
            return log.analysis_id
    
    def get_analysis_log(self, analysis_id: str) -> Optional[AnalysisLog]:
        """Recupera log de análise pelo ID"""
        if not self.analysis_collection:
            return None
        
        try:
            log_data = self.analysis_collection.find_one({"analysis_id": analysis_id})
            if log_data:
                log_data.pop("_id", None)  # Remove o _id do MongoDB
                return AnalysisLog(**log_data)
            return None
        except Exception as e:
            print(f"Erro ao recuperar log: {e}")
            return None
    
    def get_recent_analyses(self, limit: int = 10) -> List[AnalysisLog]:
        """Recupera análises recentes"""
        if not self.analysis_collection:
            return []
        
        try:
            logs_data = self.analysis_collection.find().sort("timestamp", -1).limit(limit)
            logs = []
            for log_data in logs_data:
                log_data.pop("_id", None)
                logs.append(AnalysisLog(**log_data))
            return logs
        except Exception as e:
            print(f"Erro ao recuperar análises recentes: {e}")
            return []
    
    def create_analysis_id(self) -> str:
        """Gera um ID único para análise"""
        return str(uuid.uuid4())

# Instância global do serviço
storage_service = StorageService()