from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions import from_json, col

# Downloads a library that allows Spark to read and write to Apache Kafka
spark = SparkSession.builder \
    .appName("CryptoStreamProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Defining schema structure
schema = StructType([
    StructField('symbol', StringType(), True),
    StructField('price', DoubleType(), True),
    StructField('timestamp', TimestampType(), True)
])

# Reading data from Kafka
# If Kafka has 1000 messages: "earliest" Spark will read all 1000 "latest" Spark will start with message number 1001
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "crypto_prices") \
    .option("startingOffsets", "earliest") \
    .load()

# Parsing column 'value' from bytes to string
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write function to Postgres
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/crypto_db") \
        .option("dbtable", "crypto_prices") \
        .option("user", "user") \
        .option("password", "pass") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Display result in console
query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .start()

# Wait until streaming is stopped
query.awaitTermination()
