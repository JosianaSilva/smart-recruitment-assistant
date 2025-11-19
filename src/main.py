from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes.analyze_route import router as analyze_router
from .utils.config import config

app = FastAPI(
    title="CV Analyzer",
    description="Sistema inteligente para análise automática de currículos usando OCR e LLM",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(analyze_router)

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da aplicação"""
    try:
        config.validate_config()
        return {
            "status": "healthy",
            "service": "cv-analyzer",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "CV Analyzer API",
        "description": "Sistema para análise automática de currículos",
        "endpoints": {
            "analyze": "/api/analyze",
            "history": "/api/history",
            "health": "/health"
        },
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)