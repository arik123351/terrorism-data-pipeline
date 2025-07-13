
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
    .appName("Terrorism Stream Processor") \
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
    .format("console") \
    .outputMode("append") \
    .start()

query.awaitTermination()
