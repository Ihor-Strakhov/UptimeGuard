FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# код
COPY app/ ./app

# запуск
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]