FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y curl postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# код
COPY app/ ./app

#Non-root user for security
RUN useradd -m uptimeguard && \
    chmod -R 750 /app && \
    chown -R uptimeguard:uptimeguard /app

USER uptimeguard

# запуск
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]