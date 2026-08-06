import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift
from utils.utils import *

from pyspark.sql import functions as F
from pyspark.sql.types import StringType, DateType

S3 = "s3a://st-capstone-takeo-project/data/patients"

def main():
    spark = get_spark_session()
    schema = create_schema({
        "Patient_id": StringType,
        "Patient_name": StringType,
        "patient_gender": StringType,
        "patient_birth_date": DateType,
        "patient_phone": StringType,
        "disease_name": StringType,
        "city": StringType,
        "hospital_id": StringType
        })
    df = spark.read.csv(S3, header=True, schema=schema)

    # Lower case all the columns to match redshift columns
    df = lowercase_col(df)

    # check for null
    print(count_null(df))

    # fill na
    df = fill_na(df)

    # drop duplicates
    df = drop_duplicates(df, ["patient_id"])

    write_to_redshift(df, "cleaned_data.patients")
    spark.stop()

if __name__ == '__main__':
    # spark-submit --jars ~/redshift-jdbc42-2.1.0.9.jar --packages org.apache.hadoop:hadoop-aws:3.3.4 cleansing/patients_cleanse.py
    main()