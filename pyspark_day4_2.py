from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DoubleType

from utility import *

if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

    data = [
        ("New York", 10.0),
        ("New York", 12.0),
        ("Los Angeles", 20.0),
        ("Los Angeles", 22.0),
        ("San Francisco", 15.0),
        ("San Francisco", 18.0),
    ]
    schema = create_schema({"city": StringType, "temperature": DoubleType})
    df = spark.createDataFrame(data=data, schema=schema)
    df_new = agg_function(df, "city", "temperature", ["avg", "sum", "count"])
    df_new.show(truncate=False)
    df_filter = filter_col(df_new, [("sum_temperature", ">", 30)])
    df_filter.show(truncate=False)
    sort_dataframe(df_filter, [("city", "asc")], show_result=True)
