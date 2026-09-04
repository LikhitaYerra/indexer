FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Minimal OS deps often needed by NLP/tokenizer stack.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY index_generator.py /app/index_generator.py
COPY backend/app.py /app/backend/app.py

EXPOSE 10000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "10000"]
