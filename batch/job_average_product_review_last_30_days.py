from datetime import datetime, timedelta

import redis
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, to_date

# spark-submit --master spark://spark:7077 /opt/batch/job_average_product_review_last_30_days.py

# Initialize Spark session with Hive support
spark = SparkSession.builder \
    .appName("UnitsSoldLast30Days") \
    .enableHiveSupport() \
    .config("spark.sql.warehouse.dir", "/stream/hive/warehouse") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .getOrCreate()

print("UnitsSoldLast30Days spark session started")
# Connect to Redis
redis_client = redis.Redis(host='batch-redis', port=6379, db=0)

# Load the data from Hive
df = spark.sql("SELECT ProductID, ReviewRating, TransactionDate FROM testdb.ecommerce_transactions")

df = df.withColumn("TransactionDate", to_date(col("TransactionDate")))

# Filter data for the last 30 days
current_date = datetime.now().date()
thirty_days_ago = current_date - timedelta(days=30)
df_filtered = df.filter(col("TransactionDate").between(thirty_days_ago, current_date))

# Calculate the average ReviewRating per ProductID
avg_reviews_df = df_filtered.groupBy("ProductID").agg(avg("ReviewRating").alias("AvgReviewRating"))

# avg_reviews_df.show()

# Write the result to Redis
for row in avg_reviews_df.collect():
    product_id = row["ProductID"]
    avg_rating = row["AvgReviewRating"]
    redis_client.set(f"avg_review_rating:{product_id}", avg_rating)

# Use foreachPartition to process each partition separately
# avg_reviews_df.foreachPartition(write_to_redis)

print("Average review rating per product for the last 30 days has been written to Redis")
# Stop Spark session
spark.stop()
