from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField

# Select column based on indexing
def select_col(df, fields):
    '''
         from pyspark.sql.functions import col

        df.select(col("firstname"),col("lastname")).show()

        df.select(df.columns[:3]).show()
        df.select(df.columns[2:4]).show()

    '''
    return df.select(*fields)

# Count number of rows
def count_rows(df):
    return df.count()

# Count unique rows
def count_distinct_rows(df):
    return df.distinct().count()

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
        "count": count("*").alias("count"),
        "min": min(agg_col).alias(f"min_{agg_col}"),
        "max": max(agg_col).alias(f"max_{agg_col}"),
        "avg": avg(agg_col).alias(f"avg_{agg_col}"),
        "mean": mean(agg_col).alias(f"mean_{agg_col}"),
        "sum": sum(agg_col).alias(f"sum_{agg_col}")
    }
    exprs = [agg_map[m] for m in metrics if m in agg_map]
    return df.groupBy(*group_cols).agg(*exprs)

# Group by and where clause
def filter_col(df, conditions):
    # conditions = [ ("salary", ">", 5000), ("salary", "<", 15000)]
    operators = {
        "=": lambda c, v: col(c) == v,
        "==": lambda c, v: col(c) == v,
        "!=": lambda c, v: col(c) != v,
        ">": lambda c, v: col(c) > v,
        "<": lambda c, v: col(c) < v,
        ">=": lambda c, v: col(c) >= v,
        "<=": lambda c, v: col(c) <= v,
    }

    condition = None
    for col_name, op, value in conditions:
        expr = operators[op](col_name, value)

        if condition is None:
            condition = expr
        else:
            condition = condition & expr  # AND

    return df.where(condition)


# Assigns 0 or 1 based on column value match
def assign_flag_column(df, column_name, compare_value, new_column):
    return df.select("*", when(col(column_name) != compare_value, 1).otherwise(0).alias(new_column))

# Check if row contains string for a column
def check_contain(df, column_name, compare_value, new_column):
    return df.select("*",upper(col(column_name)).contains(compare_value).alias(new_column))

# Get substring based on start and end position
def substring_col(df, column_name, first_pos, second_pos, title):
    return df.select(col(column_name).substr(first_pos, second_pos).alias(title))

# Show and count all entries in columns ["", ""]
def show_and_count_columns(df, columns):
    result = df.select(*columns)
    result.show(truncate=False)
    count_rows(result)
    return result


# Get startwith
def start_with(df, column_name, value, cols):
    return df.filter(col(column_name).startswith(value)).select(*cols)

# Get endswith
def end_with(df, column_name, value, cols):
    return df.filter(col(column_name).endswith(value)).select(*cols)

# drop columns
def drop_cols(df, cols):
    return df.drop(*cols)


# Group By
def group_and_count(df, group_column, alias_val):
    return df.groupBy(group_column).agg(count("*").alias(alias_val))
