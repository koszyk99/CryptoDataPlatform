FROM python:3.12-slim

WORKDIR /app

# Install Java (required by spark-submit inside this container) and procps
RUN apt-get update && \
    apt-get install -y default-jre procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
 
# Environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin
 
# Prevents Python logs from being buffered (show immediately in docker logs)
ENV PYTHONUNBUFFERED=1
 
# Install Python dependencies first (layer cache — only rebuilds if requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy rest of the project
COPY . .
 
# Default command: price producer
# spark-processor-job overrides this in docker-compose.yml via 'command:'
CMD ["python", "scripts/fetch_prices.py"]
