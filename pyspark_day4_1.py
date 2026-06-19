from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, DoubleType

from utility import *

if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

    data = [
        ("Smith",23,5.3 ),
        ("Rashmi",27,5.8),
        ("Smith",23,5.3 ),
        ("Payal",27,5.8 ),
        ("Megha",27,5.4 )
    ]
    schema = create_schema({"Name": StringType, "Age": IntegerType, "Height": DoubleType})
    df = spark.createDataFrame(data=data, schema=schema)
    df_dup_row = drop_duplicates(df)
    df_dup_col = drop_duplicates(df_dup_row, ["Age", "Height"])