import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift
from utils.utils import *

from pyspark.sql import functions as F

S3 = "s3a://st-capstone-takeo-project/data/disease"

def main():
    spark = get_spark_session()
    df = spark.read.csv(S3, header=True, inferSchema=True)

    # Lower case all the columns to match redshift columns
    df = lowercase_col(df)

    # strip cols
    df = df.withColumnRenamed(" disease_id", "disease_id")

    # fill na
    df = fill_na(df)

    # drop duplicates
    df = drop_duplicates(df, ["disease_id"])

    write_to_redshift(df, "cleaned_data.disease")
    spark.stop()

if __name__ == '__main__':
    # spark-submit --jars ~/redshift-jdbc42-2.1.0.9.jar --packages org.apache.hadoop:hadoop-aws:3.3.4 cleansing/disease_cleanse.py
    main()