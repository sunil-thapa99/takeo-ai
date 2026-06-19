from pyspark.sql.functions import col, lit

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
        return df.dropDuplicates()
    return df.dropDuplicates(col_names)

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