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

### Opção 1: Docker Compose

1. Configure o arquivo `.env` com suas variáveis de ambiente:
```bash
cp .env.example .env
nano .env # adicione suas variávei de ambiente usando nano ou outro editor de texto
```

2. Execute o sistema completo com Docker Compose:
```bash
# Iniciar o serviço (API + MongoDB)
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f api
docker-compose logs -f mongodb

# Parar o serviço
docker-compose down

# Parar e remover volumes (dados do MongoDB)
docker-compose down -v
```

### Opção 2: Instalação Local

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure sua GOOGLE_API_KEY no arquivo .env

## 🚀 Execução

### Com Docker Compose
```bash
# Iniciar serviços
docker-compose up -d

# Verificar status
docker-compose ps

# Acessar a API em: http://localhost:8000
# Documentação em: http://localhost:8000/docs
```

### Desenvolvimento Local
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
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
├── db/          # Script de inicialização do Banco
│   └── init_db.py
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
│   ├── config.py
│   ├── decode_toon.py
│   └── file_utils.py
└── main.py           # Aplicação principal
```