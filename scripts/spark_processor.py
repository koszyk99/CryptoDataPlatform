from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("CryptoStreamProcessor") \

    # Downloads a library that allows Spark to read and write to Apache Kafka
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \

    .getOrCreate()

# Defining schema structure
schema = StructType([
    StructField('symbol', StringType(), True),
    StructField('price', DoubleType(), True),
    StructField('timestamp', TimestampType(), True)
])

# Reading data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "crypto-topic") \

    # If Kafka has 1000 messages: "earliest" Spark will read all 1000 "latest" Spark will start with message number 1001
    .option("startingOffests", "earliest") \
    .load()
