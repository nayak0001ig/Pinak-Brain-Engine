# Use official lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (For security and network)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements first (Caching strategy)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the brain folder
COPY cloud_engine/ ./cloud_engine/

# IMPORTANT: Set Environment Variable for Python to find the module
ENV PYTHONPATH=/app

# Start command
CMD ["python", "cloud_engine/brain.py"]