import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift, read_from_redshift

from pyspark.sql import functions as F

def main():
    spark = get_spark_session()
    subscribe = read_from_redshift(spark, "cleaned_data.subscribers")
    subscribe = subscribe.withColumn(
        "age", F.floor(F.months_between(F.current_date(), F.col("birth_date"))/12)
    )
    results = (
        subscribe.filter((F.col("age") < 30) & (F.col('subgrp_id') != 'NA'))\
            .select("sub_id", "first_name", "last_name", "age", "subgrp_id")
    )
    write_to_redshift(results, '"project-output".uc02_subscribers_under30')
    results.show(truncate=False)
    spark.stop()

if __name__ == '__main__':
    main()