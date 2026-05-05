import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions import from_json, col, to_timestamp, regexp_replace

# Downloads a library that allows Spark to read and write to Apache Kafka
spark = SparkSession.builder \
    .appName("CryptoStreamProcessor") \
    .getOrCreate()

# Defining schema structure
schema = StructType([
    StructField('symbol', StringType(), True),
    StructField('price', DoubleType(), True),
    StructField('timestamp', StringType(), True)
])

# Reading data from Kafka
# If Kafka has 1000 messages: "earliest" Spark will read all 1000 "latest" Spark will start with message number 1001
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "crypto-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Parsing column 'value' from bytes to string
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn(
        "timestamp",
        to_timestamp(regexp_replace(col("timestamp"), "T", " "), "yyyy-MM-dd HH:mm:ss.SSSSSS")
    )

# Write function to Postgres
def write_to_postgres(batch_df, batch_id):

    # Retriving variables from the system (inside the container)
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    db_host = os.getenv('DB_HOST', 'postgres')
    db_port = os.getenv('DB_PORT', '5432')

    batch_df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{db_host}:{db_port}/{db_name}") \
        .option("dbtable", "crypto_prices") \
        .option("user", db_user) \
        .option("password", db_password) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Save to console
console_query = parsed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Save to Postgres
postgres_query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .start()

# Wait until streaming is stopped
spark.streams.awaitAnyTermination()
