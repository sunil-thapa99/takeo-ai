# ---- GOLD BUILD (PySpark) ----
from pyspark.sql import SparkSession, functions as F, window as W

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

BUCKET = "aws-takeo-covid-project"
SILVER = f"s3a://{BUCKET}/covid/silver"
# GOLD = f"s3a://{BUCKET}/covid/gold"
GOLD = "hdfs:///home/takeo/gold"

spark = SparkSession.builder.appName("covid-minimal-gold").getOrCreate()
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", ACCESS_KEY)
hadoop_conf.set("fs.s3a.secret.key", SECRET_KEY)
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")


# df = spark.read.parquet(f"{GOLD}/dim_date")
#
# df.show(5, False)
#
# print(df.dtypes)
#
# import pyarrow.parquet as pq
#
# table = pq.read_table("dim_date.parquet")
# print(table.schema)

cases = spark.read.parquet(f"{SILVER}/cases_standardized")
tests = spark.read.parquet(f"{SILVER}/testing_standardized")

# dim_date
all_dates = (cases.select("full_date").union(tests.select("full_date")).dropDuplicates())
dim_date = (all_dates
  .withColumn("date_id", F.date_format("full_date", "yyyyMMdd").cast("int"))
  .withColumn("year", F.year("full_date"))
  .withColumn("month", F.month("full_date"))
  .withColumn("day", F.dayofmonth("full_date"))
  .withColumn("dow", F.dayofweek("full_date"))
  .withColumn("is_weekend", F.dayofweek("full_date").isin([1, 7]))
)

dim_date.write.mode("overwrite").parquet(f"{GOLD}/dim_date")


# dim_state
dim_state = cases.select("state_code", "state_name").dropDuplicates()
dim_state.write.mode("overwrite").parquet(f"{GOLD}/dim_state")

# fact_cases_state_daily
w = W.Window.partitionBy("state_code").orderBy("full_date")
fact_cases = (cases
  .withColumn("date_id", F.date_format("full_date", "yyyyMMdd").cast("int"))
  .withColumn("new_cases",  F.greatest(F.col("cases_cum")  - F.lag("cases_cum").over(w),  F.lit(0)))
  .withColumn("new_deaths", F.greatest(F.col("deaths_cum") - F.lag("deaths_cum").over(w), F.lit(0)))
  .select("date_id", "state_code", "cases_cum", "deaths_cum", "new_cases", "new_deaths")
)
fact_cases.write.mode("overwrite").parquet(f"{GOLD}/fact_cases_state_daily")

# fact_testing_state_daily
w2 = W.Window.partitionBy("state_code").orderBy("full_date")
fact_tests = (tests
  .withColumn("date_id", F.date_format("full_date", "yyyyMMdd").cast("int"))
  .withColumn("new_tests", F.greatest(F.col("tests_total_cum") - F.lag("tests_total_cum").over(w2), F.lit(0)))
  .withColumn("positivity_rate", F.when(F.col("tests_total_cum") > 0,
                                       (F.col("tests_pos_cum") / F.col("tests_total_cum")).cast("double")))
  .select("date_id", "state_code", "tests_total_cum", "tests_pos_cum", "tests_neg_cum", "new_tests", "positivity_rate")
)
fact_tests.write.mode("overwrite").parquet(f"{GOLD}/fact_testing_state_daily")

print("Gold complete.")
