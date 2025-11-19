from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from ..services.analysis_service import analysis_service
from ..models.cv_model import CVResponse
from ..models.analysis_model import AnalysisLog

router = APIRouter(prefix="/api", tags=["CV Analysis"])

@router.post("/analyze", response_model=CVResponse)
async def analyze_cvs(
    files: List[UploadFile] = File(..., description="Arquivos de CV (PDF, JPEG, PNG)"),
    query: Optional[str] = Form(None, description="Pergunta ou critério de análise")
):
    """Analisa CVs e retorna sumários ou comparações baseadas na query.
    
    Args:
        files: Lista de arquivos de CV (PDF, JPEG, PNG)
        query: Pergunta opcional para análise específica ou comparação
    
    Returns:
        CVResponse: Resultado da análise com sumários ou comparações
    
    Examples:
        - Sem query: Retorna resumos de todos os CVs
        - Com query "Quem tem mais experiência?": Compara candidatos
        - Com query "Quem sabe Python?": Filtra por skills específicas
    """
    if not files:
        raise HTTPException(status_code=400, detail="Pelo menos um arquivo deve ser enviado")
    
    try:
        result = await analysis_service.analyze_cvs(files, query)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/history", response_model=List[AnalysisLog])
async def get_analysis_history(limit: int = 10):
    """Recupera histórico de análises realizadas.
    
    Args:
        limit: Número máximo de análises a retornar (padrão: 10)
    
    Returns:
        List[AnalysisLog]: Lista de análises realizadas
    """
    try:
        history = analysis_service.get_analysis_history(limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar histórico: {str(e)}")

@router.get("/analysis/{analysis_id}", response_model=AnalysisLog)
async def get_analysis_by_id(analysis_id: str):
    """Recupera análise específica por ID.
    
    Args:
        analysis_id: ID único da análise
    
    Returns:
        AnalysisLog: Dados da análise solicitada
    """
    try:
        analysis = analysis_service.get_analysis_by_id(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Análise não encontrada")
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar análise: {str(e)}")