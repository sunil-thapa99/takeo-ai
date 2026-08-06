import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift, read_from_redshift

from pyspark.sql import functions as F

def main():
    spark = get_spark_session()
    grpsubgrp = read_from_redshift(spark, "cleaned_data.grpsubgrp")
    grp = read_from_redshift(spark, "cleaned_data.groups")
    
    results = (
        grpsubgrp.groupBy("grp_id")\
        .agg(F.count_distinct("subgrp_id").alias("subgrp_count"))\
        .join(grp.select("grp_id", "grp_name"), "grp_id", "left")\
        .orderBy(F.desc("subgrp_count"))
    )
    write_to_redshift(results, '"project-output".uc03_group_max_subgroups')
    results.show(truncate=False)
    spark.stop()

if __name__ == '__main__':
    main()