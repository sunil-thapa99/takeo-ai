from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType

from utility import *

if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    print()