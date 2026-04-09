# Dockerfile — FastAPI (API de mensagens)
FROM python:3.11-slim

WORKDIR /app

# Dependências de sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia módulos necessários para a API
COPY database.py .
COPY shared_state.py .
COPY analysis.py .
COPY neo4j_graph.py .
COPY api.py .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
