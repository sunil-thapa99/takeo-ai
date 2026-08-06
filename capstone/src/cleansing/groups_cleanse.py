import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift
from utils.utils import *

from pyspark.sql import functions as F
from pyspark.sql.types import StringType, DateType

S3 = "s3a://st-capstone-takeo-project/data/groups"

def main():
    spark = get_spark_session()
    df = spark.read.csv(S3, header=True, inferSchema=True)

    # Lower case all the columns to match redshift columns
    df = lowercase_col(df)

    # fill na
    df = fill_na(df)

    # drop duplicates
    df = drop_duplicates(df, ["grp_id"])

    # Update type
    df = df.withColumn("premium_written", F.col("premium_written").cast("decimal(12,2)"))
    df = df.withColumn("year", F.col("year").cast("integer"))

    write_to_redshift(df, "cleaned_data.groups")
    spark.stop()

if __name__ == '__main__':
    # spark-submit --jars ~/redshift-jdbc42-2.1.0.9.jar --packages org.apache.hadoop:hadoop-aws:3.3.4 cleansing/gruops_cleanse.py
    main()