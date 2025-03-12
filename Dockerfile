FROM python:3.11-slim

WORKDIR /app

# Copia primeiro o requirements.txt para aproveitar o cache do Docker
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "Principal.py"]