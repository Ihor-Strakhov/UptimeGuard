FROM python:3.12-slim

WORKDIR /app

# зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# код
COPY app/ ./app

# запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]