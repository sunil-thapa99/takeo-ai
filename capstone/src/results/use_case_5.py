import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift, read_from_redshift

from pyspark.sql import functions as F

def main():
    spark = get_spark_session()
    subscribers = read_from_redshift(spark, "cleaned_data.subscribers")
    subgroups = read_from_redshift(spark, "cleaned_data.subgroups")
    
    results = (
        subscribers.groupBy("subgrp_id")\
        .agg(F.count("sub_id").alias("subscription_count"))\
        .join(subgroups.select("subgrp_id", "subgrp_name"), "subgrp_id", "left")\
        .orderBy(F.desc("subscription_count"))
    )
    write_to_redshift(results, '"project-output".uc05_most_subscribed_subgroup')
    results.show(truncate=False)
    spark.stop()

if __name__ == '__main__':
    main()