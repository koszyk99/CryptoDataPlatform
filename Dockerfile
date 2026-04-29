FROM python:3.12-slim

WORKDIR /app

# Installing Java and procps (for Spark)
RUN apt-get update && \
    apt-get install -y default-jre procps && \
    apt-get clean

# Setting environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin
# Prevents Python logs from being cached
ENV PYTHONUNBUFFERED=1

# Copy rest of the files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Start command
CMD ["python", "scripts/fetch_prices.py"]
