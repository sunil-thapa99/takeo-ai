import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift
from utils.utils import *

from pyspark.sql import functions as F
from pyspark.sql.types import StringType, DateType

S3 = "s3a://st-capstone-takeo-project/data/subscribers"

def main():
    spark = get_spark_session()
    df = spark.read.csv(S3, header=True, inferSchema=True)

    # Strip cols
    df = strip_col(df)

    # Lower case all the columns to match redshift columns
    df = lowercase_col(df)

    # fill na
    df = fill_na(df)

    # drop duplicates
    df = drop_duplicates(df, ["sub_id"])

    # Update type
    df = df.withColumn("eff_date", F.to_date(F.col("eff_date"), "yyyy-MM-dd"))
    df = df.withColumn("birth_date", F.to_date(F.col("birth_date"), "yyyy-MM-dd"))
    df = df.withColumn("term_date", F.to_date(F.col("term_date"), "yyyy-MM-dd"))

    write_to_redshift(df, "cleaned_data.subscribers")
    spark.stop()

if __name__ == '__main__':
    # spark-submit --packages org.apache.hadoop:hadoop-aws:3.3.4 cleansing/subscribers_cleanse.py
    main()