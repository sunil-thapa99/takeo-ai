import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.spark_sessions import get_spark_session, write_to_redshift, read_from_redshift

from pyspark.sql import functions as F

def main():
    spark = get_spark_session()
    patient = read_from_redshift(spark, "cleaned_data.patients")
    hospital = read_from_redshift(spark, "cleaned_data.hospitals")
    
    results = (
        patient.groupBy("hospital_id")\
        .agg(F.count("patient_id").alias("patient_count"))\
        .join(hospital.select("hospital_id", "hospital_name"), "hospital_id", "left")\
        .orderBy(F.desc(F.col("patient_count")))
    )
    write_to_redshift(results, '"project-output".uc04_hospital_most_patients')
    results.show(truncate=False)
    spark.stop()

if __name__ == '__main__':
    main()