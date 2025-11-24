FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

COPY .env ./

RUN mkdir -p /tmp/cv_analyzer

ENV PYTHONPATH=/app
ENV TMPDIR=/tmp/cv_analyzer

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]