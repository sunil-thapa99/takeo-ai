from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField
from pyspark.sql import functions as F

# Select column based on indexing
def select_col(df, fields):
    '''
         from pyspark.sql.functions import col

        df.select(col("firstname"),col("lastname")).show()

        df.select(df.columns[:3]).show()
        df.select(df.columns[2:4]).show()

    '''
    return df.select(*fields)

# Transform column type
def transform_col(df, col_name, new_col_name, transform):
    return df.withColumn(new_col_name, col(col_name).cast(transform))

# Multiply value of a column by certain number
def update_col(df, col_name, new_col_name, update):
    return df.withColumn(new_col_name, col(col_name)*update)

# Add a constant value to a column
def add_col(df, col_name, const_val):
    return df.withColumn(col_name, lit(const_val))

# Drop duplicate values from single or multiple columns
def drop_duplicates(df, col_names=None):
    # Use: drop_duplicates(df, ["department"])

    if col_names is None:
        df_dup = df.dropDuplicates()
    else:
        df_dup = df.dropDuplicates(col_names)

    df_dup.show(truncate=False)
    return df_dup

# Sort column's based on Asc or Desc
def sort_dataframe(df, sort_specs, show_result=True, truncate=False):
    # Use: sort_dataframe(df, [("department", "asc"), ("state", "asc")])
    sort_express = [
        col(column).asc() if direction.lower() == "asc"
        else col(column).desc()
        for column, direction in sort_specs
    ]

    sorted_df = df.orderBy(*sort_express)

    if show_result:
        sorted_df.show(truncate=truncate)

    return sorted_df

# Define columns with type on schema
def create_schema(columns: dict):
    return StructType([
        StructField(column, dtype(), True)
        for column, dtype in columns.items()
    ])

# Apply aggregate function
def agg_function(df, group_cols, agg_col, metrics):
    if isinstance(group_cols, str):
        group_cols = [group_cols]

    agg_map = {
        "count": F.count("*").alias("count"),
        "min": F.min(agg_col).alias(f"min_{agg_col}"),
        "max": F.max(agg_col).alias(f"max_{agg_col}"),
        "avg": F.avg(agg_col).alias(f"avg_{agg_col}"),
        "mean": F.mean(agg_col).alias(f"mean_{agg_col}"),
        "sum": F.sum(agg_col).alias(f"sum_{agg_col}")
    }
    exprs = [agg_map[m] for m in metrics if m in agg_map]
    return df.groupBy(*group_cols).agg(*exprs)

# Group by and where clause
def filter_col(df, conditions):
    # conditions = [ ("salary", ">", 5000), ("salary", "<", 15000)]
    operators = {
        "=": lambda c, v: F.col(c) == v,
        "==": lambda c, v: F.col(c) == v,
        "!=": lambda c, v: F.col(c) != v,
        ">": lambda c, v: F.col(c) > v,
        "<": lambda c, v: F.col(c) < v,
        ">=": lambda c, v: F.col(c) >= v,
        "<=": lambda c, v: F.col(c) <= v,
    }

    condition = None
    for col_name, op, value in conditions:
        expr = operators[op](col_name, value)

        if condition is None:
            condition = expr
        else:
            condition = condition & expr  # AND

    return df.where(condition)