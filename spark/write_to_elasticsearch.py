
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

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
])

spark = SparkSession.builder \
    .appName("Write to Elasticsearch") \
    .config("spark.es.nodes", "localhost") \
    .config("spark.es.port", "9200") \
    .config("spark.es.resource", "terrorism/_doc") \
    .config("spark.es.nodes.wan.only", "true") \
    .getOrCreate()

lines = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "terrorism") \
    .load()

df = lines.selectExpr("CAST(value AS STRING)")
json_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

enriched_df = json_df.withColumn("casualties", col("nkill") + col("nwound"))

query = enriched_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .option("es.resource", "terrorism/_doc") \
    .start()

query.awaitTermination()