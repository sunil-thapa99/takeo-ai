from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, DoubleType

from utility import *


if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    file_path = "file:///home/takeo/pycharmproject/project6-Covid-19_data_analysis/CovidCases.csv"
    format_file = 'csv'
    df = read(spark, format_type=format_file, file_path=file_path,
              header=True, infer_schema=True)
    df.show(10, truncate=False)
    df = transform_col(df, "confirmed", "confirmed", "Integer")
    df_grouped = agg_function(df, ["province", 'city'], "confirmed", ["sum", "max"])
    df_grouped = df_grouped.withColumnRenamed("sum_confirmed", "TotalConfirmed")
    df_grouped = df_grouped.withColumnRenamed("max_confirmed", "MaxFromOneConfirmedCase")
    df_sort = sort_dataframe(df_grouped, [("TotalConfirmed", "asc")], show_result=True)

    # Section 2
    total_cases = agg_function(df, ['province'], 'confirmed', ['sum'])
    total_cases_desc = sort_dataframe(total_cases, [("sum_confirmed", "desc")], show_result=False)
    total_cases_desc.limit(2).show()

    # Section 3
    df_filter = filter_col(df, [("province", "==", "Daegu"), ("confirmed", ">", 10)])
    df_filter.show(10, truncate=False)

    # given hint
    drop_list = ['latitude', 'longitude', 'case_id', ]
    df_new = df.select([column for column in df.columns if column not in drop_list])
    df_new.show(10, truncate=False)

    # My Function
    df_old = drop_cols(df, drop_list)
    df_old.show(10, truncate=False)



