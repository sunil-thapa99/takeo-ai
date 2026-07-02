from pyspark.sql.functions import col, count, countDistinct, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql import SparkSession
import os

if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    df = spark.read.format("csv").options(header=True, inferSchema=True, delimiter=',').load(
        'file:///home/takeo/pycharmproject/pyspark/project7-airport/airports.csv')

    # count airports that are present in South east part assuming Papua New Guinea lies in south east
    df_se = df.filter(
        col("Country").isin(["Papua New Guinea"])
    ).groupBy("Country").agg(count(col('*')).alias("Southeast airport Country"))
    # df_se.write.mode("overwrite").option("header", "true").csv("hdfs:///home/takeo/airports")

    # Find out how many unique cities have airports in each country
    df_unique_cities = df.groupBy(col("Country")).agg(countDistinct("City"))
    # df_unique_cities.write.mode("overwrite").option("header", "true").csv("hdfs:///home/takeo/airports_unique_cities")

    # What is the average altitude (in feet) of airports in each country
    df_avg_alt = df.groupBy(col("Country")).agg(avg("Altitude"))
    df_avg_alt.write.mode("overwrite").option("header", "true").csv("hdfs:///home/takeo/airports_avg_alt")

    # Find out in each timezones how many airports are operating