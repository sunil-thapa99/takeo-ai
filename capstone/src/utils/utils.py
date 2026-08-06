from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField
from pyspark.sql import DataFrame 

def drop_duplicates(df, col_names=None):
    # Use: drop_duplicates(df, ["department"])

    if col_names is None:
        df_dup = df.dropDuplicates()
    else:
        df_dup = df.dropDuplicates(col_names)

    # df_dup.show(truncate=False)
    return df_dup

def count_null(df):
    for c in df.columns:
        print(f"{c}: {df.filter(col(c).isNull()).count()} nulls")

def fill_na(df):
    return df.fillna("NA")

# Define columns with type on schema
def create_schema(columns: dict):
    return StructType([
        StructField(column, dtype(), True)
        for column, dtype in columns.items()
    ])

# Rename to lower-case
def lowercase_col(df: DataFrame):
    return df.toDF(*[col.lower() for col in df.columns])

# strip space on column name
def strip_col(df: DataFrame):
    return df.toDF(*[col.strip() for col in df.columns])