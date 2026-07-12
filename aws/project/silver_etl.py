# spark-submit --packages org.apache.hadoop:hadoop-aws:3.3.4 silver_etl.py

from pyspark.sql import SparkSession, functions as F

import os
import subprocess
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

spark = SparkSession.builder.appName("covid-minimal-silver").getOrCreate()
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", ACCESS_KEY)
hadoop_conf.set("fs.s3a.secret.key", SECRET_KEY)
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

BUCKET = "aws-takeo-covid-project"
BRONZE = f"s3a://{BUCKET}/covid/bronze"
SILVER = f"s3a://{BUCKET}/covid/silver"

# Helpers
upper_trim = lambda c: F.upper(F.trim(F.col(c)))
to_date = lambda c: F.to_date(F.col(c).cast("string"))

# --- Lookups ---
states = (spark.read.option("header", True).csv(f"{BRONZE}/static/states_abv.csv")
          .select(upper_trim("Abbreviation").alias("state_code"), F.initcap("State").alias("state_name")))

# --- Cases (NYT state file: date,state,cases,deaths or JHU state-level variant) ---
cases_raw = spark.read.option("header", True).csv(f"{BRONZE}/nytimes/us_states.csv")

cases_std = (cases_raw
  # Handle date formats like "2020-05-01" or yyyymmdd; adjust if needed
  .withColumn("full_date", F.to_date("date"))
  # If the file stores state NAME, map to code; if it already stores code, this join still works
  .withColumn("state_name_raw", F.initcap(F.col("state")))
  .join(states, states.state_name == F.col("state_name_raw"), "left")
  .withColumn("cases_cum", F.col("cases").cast("long"))
  .withColumn("deaths_cum", F.col("deaths").cast("long"))
  .withColumn("year", F.year("full_date"))
  .withColumn("month", F.month("full_date"))
  .withColumn("day", F.dayofmonth("full_date"))
  .select("full_date", "state_code", "state_name", "cases_cum", "deaths_cum", "year", "month", "day")
  .dropna(subset=["full_date", "state_code"])
)

(cases_std.write.mode("overwrite")
  .partitionBy("state_code", "year", "month", "day")
  .parquet(f"{SILVER}/cases_standardized"))


# --- Testing (COVID Tracking: date(int yyyymmdd), state(code), positive, negative, totalTestResults) ---
tests_raw = spark.read.option("header", True).csv(f"{BRONZE}/covid_tracking/states_daily.csv")

tests_std = (tests_raw
  .withColumn("full_date", F.to_date(F.col("date").cast("string"), "yyyyMMdd"))
  .withColumn("state_code", upper_trim("state"))
  .join(states.select("state_code", "state_name"), "state_code", "left")
  .withColumn("tests_total_cum", F.col("totalTestResults").cast("long"))
  .withColumn("tests_pos_cum", F.col("positive").cast("long"))
  .withColumn("tests_neg_cum", F.col("negative").cast("long"))
  .withColumn("year", F.year("full_date"))
  .withColumn("month", F.month("full_date"))
  .withColumn("day", F.dayofmonth("full_date"))
  .select("full_date", "state_code", "state_name", "tests_total_cum", "tests_pos_cum", "tests_neg_cum", "year", "month", "day")
  .dropna(subset=["full_date", "state_code"])
)

(tests_std.write.mode("overwrite")
  .partitionBy("state_code", "year", "month", "day")
  .parquet(f"{SILVER}/testing_standardized"))

print("Silver complete.")
