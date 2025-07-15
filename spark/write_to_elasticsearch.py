from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, current_timestamp
from pyspark.sql.types import *

def write_to_elasticsearch():
    """Write stream data to Elasticsearch with optimized configurations"""
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

    spark = SparkSession.builder \
        .appName("Write to Elasticsearch") \
        .config("spark.es.nodes", "localhost") \
        .config("spark.es.port", "9200") \
        .config("spark.es.resource", "terrorism/_doc") \
        .config("spark.es.batch.size.entries", "1000") \
        .config("spark.es.batch.size.bytes", "1mb") \
        .config("spark.es.batch.write.refresh", "false") \
        .getOrCreate()

    lines = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "terrorism") \
        .option("startingOffsets", "latest") \
        .load()

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

    # Write to Elasticsearch with optimized settings
    query = enriched_df.writeStream \
        .format("org.elasticsearch.spark.sql") \
        .option("checkpointLocation", "/tmp/elasticsearch_checkpoint") \
        .option("es.resource", "terrorism/_doc") \
        .option("es.mapping.id", "eventid") \
        .trigger(processingTime='30 seconds') \
        .start()

if __name__ == "__main__":
    write_to_elasticsearch()
