FROM python:3.12-slim

WORKDIR /app

# Copy the installation script and give it permissions
COPY scripts/install_java.sh ./scripts/
RUN chmod +x ./scripts/install_java.sh

# Run script inside the image
RUN ./scripts/install_java.sh

# Setting environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Copy rest of the files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Start command
CMD ["python", "scripts/fetch_prices.py"]
