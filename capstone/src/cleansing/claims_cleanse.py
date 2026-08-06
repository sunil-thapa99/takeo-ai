import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift
from utils.utils import *

from pyspark.sql import functions as F

S3 = "s3a://st-capstone-takeo-project/data/claims/claims.json"

def main():
    spark = get_spark_session()
    df = spark.read.json(S3)

    # Lower case all the columns to match redshift columns
    df = lowercase_col(df)

    # Replace NaN with NA
    df = df.withColumn("claim_or_rejected",
                       F.when(F.col("claim_or_rejected") == "NaN", "NA")\
                        .otherwise(F.col("claim_or_rejected")))

    # fill na
    df = fill_na(df)

    # drop duplicates
    df = drop_duplicates(df, ["claim_id"])

    # Update type
    df = df.withColumn("claim_amount", F.col("claim_amount").cast("decimal(12,2)"))
    df = df.withColumn("claim_date", F.to_date(F.col("claim_date"), "yyyy-MM-dd"))
    df = df.withColumn("patient_id", F.col("patient_id").cast("string"))

    write_to_redshift(df, "cleaned_data.claims")
    spark.stop()

if __name__ == '__main__':
    # spark-submit --jars ~/redshift-jdbc42-2.1.0.9.jar --packages org.apache.hadoop:hadoop-aws:3.3.4 cleansing/claims_cleanse.py
    main()