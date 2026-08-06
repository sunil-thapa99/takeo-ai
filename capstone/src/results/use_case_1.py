import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift, read_from_redshift

from pyspark.sql import functions as F

def main():
    spark = get_spark_session()
    claims = read_from_redshift(spark, "cleaned_data.claims")

    results = (
        claims.groupBy("disease_name")\
        .agg(F.count("claim_id").alias("claim_count"))\
        .orderBy(F.desc("claim_count"), F.asc("disease_name"))
    )
    write_to_redshift(results, '"project-output".uc01_max_claims_disease')
    results.show(truncate=False)
    spark.stop()

if __name__ == '__main__':
    main()