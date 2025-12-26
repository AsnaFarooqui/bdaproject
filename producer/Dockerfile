# Base image (lightweight, stable)
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy generator code
COPY generator.py .
COPY schemas.py .
COPY models ./models

# Environment variable for Kafka (used later)
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Run the generator
CMD ["python", "generator.py"]

