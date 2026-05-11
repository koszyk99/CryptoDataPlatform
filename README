CryptoDataPlatform

A comprehensive system for real-time streaming and analysis of cryptocurrency data. The project utilizes the modern Data Lakehouse architecture, integrating data retrieval via APIs, messaging via Kafka, stream processing in Spark, and visualization in Grafana.

System Architecture

The system consists of the following components:

Price Producer (Python): Retrieves cryptocurrency price data from external APIs and sends it to a topic in Kafka.

Apache Kafka: A message broker serving as a buffer for incoming data.

Apache Spark (PySpark): A distributed processing engine that consumes data from Kafka, performs transformations (e.g., temporal aggregations), and stores the results in a database.

PostgreSQL: A relational database storing processed historical and current data.

Grafana: An analytics and visualization tool that allows you to create interactive dashboards.

Technology Stack

Language: Python 3.12

Data Processing: Apache Spark 3.5.1

Streaming: Apache Kafka & KRaft

Database: PostgreSQL 15

Visualization: Grafana

Containerization: Docker & Docker Compose

Project Launch

Requirements

Docker and Docker Compose installed.

Steps

Clone the repository:

git clone <link-to-your-repo>
cd CryptoDataPlatform


Configure environment variables:
Make sure the .env file contains the correct database credentials and API keys.

Start the infrastructure:

docker compose up --build


Access to services:

Grafana: http://localhost:3000 (Login: admin, Password: admin)

Kafka UI: http://localhost:8080

Spark Master: http://localhost:8081

Configuring Grafana

To view graphs:

Log in to Grafana.

Add a new data source (PostgreSQL).

Enter postgres:5432 as the host.

Create a new Dashboard and use an SQL query, e.g.:

SELECT timestamp AS "time", price, symbol FROM crypto_prices WHERE $__timeFilter(timestamp);


Troubleshooting

Spark-submit error: If the spark-processor-job container reports a missing executable, ensure that the path in docker-compose.yml points to /opt/bitnami/spark/bin/spark-submit.

Missing data in Grafana: Check the producer logs (docker logs price-producer) and Spark logs (docker logs spark-processor-job) to ensure that data is flowing through the system.

This project was created for educational purposes – real-time data streaming analysis.
