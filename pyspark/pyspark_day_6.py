import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, DoubleType

from utility import *

if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'zipcodes.csv')
    out_path = '/tmp/spark_output/zipcodes'
    format_file = 'csv'
    df = read(spark, format_type=format_file ,file_path=file_path,
              header=True, infer_schema=True)
    df.show()

    write(df, 'csv', out_path)