import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift
from utils.utils import *

from pyspark.sql import functions as F

S3 = "s3a://st-capstone-takeo-project/data/hospital"

def main():
    spark = get_spark_session()
    df = spark.read.csv(S3, header=True, inferSchema=True)

    # Strip, Lower case all the columns to match redshift columns
    df = strip_col(df)
    df = lowercase_col(df)

    # fill na
    df = fill_na(df)

    # drop duplicates
    df = drop_duplicates(df, ["hospital_id"])

    write_to_redshift(df, "cleaned_data.hospital")
    spark.stop()

if __name__ == '__main__':
    # spark-submit --packages org.apache.hadoop:hadoop-aws:3.3.4 cleansing/hospitals_cleanse.py
    main()