# CV Analyzer - Sistema Inteligente de Análise de Currículos

Sistema para análise automática de currículos usando OCR (EasyOCR) e LLM (Google Gemini). Processa PDFs e imagens, extrai texto, gera sumários estruturados e permite consultas comparativas entre candidatos.

## 🚀 Funcionalidades

- **Processamento de Arquivos**: Suporte a PDF, JPEG, PNG
- **OCR**: Extração de texto com EasyOCR e fallback para PyMuPDF
- **Análise com IA**: Sumários e comparações usando Google Gemini
- **API REST**: Interface completa com FastAPI
- **Logging**: Armazenamento de análises no MongoDB (opcional)

## 📋 Pré-requisitos

- Python 3.8+
- Google AI API Key (Gemini)
- MongoDB (opcional, para logging)

## 🛠️ Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure sua GOOGLE_API_KEY no arquivo .env

## 🚀 Execução

### Desenvolvimento
```bash
cd src
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Produção
```bash
cd src
python main.py
```

## 📚 Uso da API

### Análise de CVs
```bash
POST /api/analyze
```

**Exemplos:**

Análise simples (apenas resumos):
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "files=@cv1.pdf" \
  -F "files=@cv2.pdf"
```

Comparação entre candidatos:
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "files=@cv1.pdf" \
  -F "files=@cv2.pdf" \
  -F "query=Quem tem mais experiência em Python?"
```

### Outros endpoints
- `GET /api/history` - Histórico de análises
- `GET /api/analysis/{id}` - Análise específica
- `GET /health` - Health check
- `GET /docs` - Documentação da API

## 🏗️ Arquitetura

```
src/
├── services/          # Lógica de negócio
│   ├── ocr_service.py      # Processamento OCR
│   ├── llm_service.py      # Integração com Gemini
│   ├── storage_service.py  # Persistência MongoDB
│   └── analysis_service.py # Orquestração principal
├── routes/            # Endpoints da API
│   └── analyze_route.py
├── models/            # Modelos de dados
│   ├── cv_model.py
│   └── analysis_model.py
├── utils/             # Utilitários
│   ├── file_utils.py
│   └── config.py
└── main.py           # Aplicação principal
```