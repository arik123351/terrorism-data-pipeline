from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, current_timestamp, year, month, dayofmonth
from pyspark.sql.types import *

def create_spark_session():
    """Create Spark session with optimized configurations"""
    return SparkSession.builder \
        .appName("Terrorism Stream Processor") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def process_stream():
    """Process Kafka stream with enhanced transformations"""
    schema = StructType([
        StructField("eventid", StringType(), True),
        StructField("iyear", IntegerType(), True),
        StructField("imonth", IntegerType(), True),
        StructField("iday", IntegerType(), True),
        StructField("country_txt", StringType(), True),
        StructField("region_txt", StringType(), True),
        StructField("attacktype1_txt", StringType(), True),
        StructField("nkill", IntegerType(), True),
        StructField("nwound", IntegerType(), True),
        StructField("timestamp", StringType(), True),
    ])

    spark = create_spark_session()
    
    # Read from Kafka
    lines = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "terrorism") \
        .option("startingOffsets", "latest") \
        .load()

    # Parse JSON and apply transformations
    df = lines.selectExpr("CAST(value AS STRING)")
    json_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

    # Enhanced data processing
    enriched_df = json_df \
        .withColumn("casualties", col("nkill") + col("nwound")) \
        .withColumn("severity_level", 
                   when(col("casualties") == 0, "Low")
                   .when(col("casualties") <= 10, "Medium")
                   .when(col("casualties") <= 50, "High")
                   .otherwise("Critical")) \
        .withColumn("processed_timestamp", current_timestamp())
    
    # Write to console with formatted output
    query = enriched_df.writeStream \
        .format("console") \
        .outputMode("append") \
        .trigger(processingTime='10 seconds') \
        .option("truncate", "false") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    process_stream()