FROM python:3.11-slim

WORKDIR /app

# Install build tools (safer in case frontend also needs native deps)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./frontend-service/ /app/

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
