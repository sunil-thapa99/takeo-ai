from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, StringType, LongType

if __name__ == '__main__':
    spark = SparkSession.builder.appName("APILog").getOrCreate()
    cols = StructType([
        StructField("ip_address", StringType(), True),
        StructField("client_identd", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("date", StringType(), True),
        StructField("time", StringType(), True),
        StructField("method", StringType(), True),
        StructField("endpoint", StringType(), True),
        StructField("protocol", StringType(), True),
        StructField("response_code", LongType(), True),
        StructField("content_size", LongType(), True),
    ])
    df = spark.read.format('parquet').options(header=True, inferSchema=True).schema(cols).load('file:///home/takeo/pycharmproject/project9-anomalies-actual-project/apilogs.parquet')

    # Section 1:
    # Top 10 endpoints which transfer maximum content in kb
    top_10_endpoints = df.groupBy('endpoint')\
        .agg(F.round(F.sum('content_size')/1024).alias("total_content"))\
            .orderBy(F.desc("total_content")).limit(10)
    top_10_endpoints.show(truncate=False)

    # Top 10 visited endpoints
    top_10_visited = df.groupBy('endpoint')\
        .agg(F.count("*").alias('visited_endpoints'))\
        .orderBy(F.desc("visited_endpoints")).limit(10)
    top_10_visited.show(truncate=False)

    # List down the day and its visited content size
    day_content_size = df.groupBy('date')\
        .agg(F.sum("content_size").alias("content_size"), 
            F.round(F.sum("content_size")/1024, 2).alias("total_content_size_kb"))\
            .orderBy("date")
    day_content_size.show(truncate=False)

    # Min content size, Max content size, Count content size
    content_size_stats = df.select(
        F.min("content_size").alias("min_content_size"),
        F.max("content_size").alias("max_content_size"),
        F.count("content_size").alias("total_count_content_size"),
    )
    content_size_stats.show(truncate=False)


    # Section 2:
    # Response Code Analysis > Response Codes with Number of Codes
    response_code_analysis = df.groupBy("response_code")\
        .agg(F.count("*").alias("total_number_codes"))\
        .orderBy(F.desc("total_number_codes"))
    response_code_analysis.show(truncate=False)

    # Any IPAddress that has accessed the server more than 10 times
    ip_access = df.groupBy("ip_address")\
            .agg(F.count("*").alias("visit_count"))\
            .filter(F.col("visit_count") > 10)\
            .orderBy(F.desc("visit_count"))
    ip_access.show(truncate=False)

    # Most Frequent Visitors (visited at least 10 times, ordered by frequency)
    ip_visitor = df.groupBy("ip_address")\
                .agg(F.count("*").alias("visit_count"))\
                .filter(F.col("visit_count") >= 10)\
                .orderBy(F.desc("visit_count"))
    ip_visitor.show(truncate=False)

    # Section 3:
    # Top 10 latest 404 requests with their endpoints and time
    latest_404_requests = (
        df.filter(F.col("response_code") == 404)
        .withColumn(
            "full_timestamp",
            F.to_timestamp(F.concat_ws(" ", F.col("date"), F.col("time"))),
        )
        .orderBy(
            F.col("full_timestamp").desc_nulls_last(),
            F.col("date").desc(),
            F.col("time").desc(),
        )
        .select("ip_address", "endpoint", "date", "time", "response_code")
        .limit(10)
    )
    latest_404_requests.show(truncate=False)
