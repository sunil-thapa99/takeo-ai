from pyspark.sql.functions import col, to_date

def bronze_ingestion(spark, csv_path, table_name):
    """
        This function is used to ingest a csv file

        :param spark: spark session object
        :param csv_path: file path
        :param table_name: String

        :return: table name: String
    """
    df = (spark.read.option("header", "true").csv(csv_path))
    df.write.mode("overwrite").format("parquet").saveAsTable(f"iphone_analytics.bronze_{table_name}")
    return f"bronze_{table_name}"

def silver_sales_transform_partition(spark, df_name, transformation_column, store_table_name, partition_column, file_format):
    """
    This function converts column data type and stores into table as partition

    :param df: spark dataframe
    :param store_table_name, partition_column, file_format: String
    :param transformation_column: dict {"col1": "int", "col2": "date"}

    :return: Stored table name: String
    """
    df = spark.table(df_name)
    for key, value in transformation_column.items():
        if value == "date":
            df = df.withColumn(key, to_date(col(key)))
        else:
            df = df.withColumn(key, col(key).cast(value))
    df.write.mode("overwrite").partitionBy(partition_column).format(file_format).saveAsTable(f"iphone_analytics.{store_table_name}")
    return store_table_name


def silver_sales_transform(spark, df_name, transformation_column, store_table_name, file_format):
    """
    This function converts column data type and stores into table as partition

    :param df: spark dataframe
    :param store_table_name, file_format: String
    :param transformation_column: dict {"col1": "int", "col2": "date"}

    :return: Stored table name: String
    """
    df = spark.table(df_name)
    for key, value in transformation_column.items():
        if value == "date":
            df = df.withColumn(key, to_date(col(key)))
        else:
            df = df.withColumn(key, col(key).cast(value))
    df.write.mode("overwrite").format(file_format).saveAsTable(f"iphone_analytics.{store_table_name}")
    return store_table_name

