from pyspark.sql import SparkSession
from bronze_silver.iphone_sales_project import bronze_silver
from gold.fact_load import *


if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName(
        "bootcamp.com").enableHiveSupport().getOrCreate()
    bronze_silver(spark)

    load_fact_store(spark)
    load_fact_product(spark)
    load_fact_customer(spark)
    load_fact_sales(spark)