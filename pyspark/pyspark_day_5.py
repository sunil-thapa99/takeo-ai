import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, DoubleType

from utility import *

if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

    books_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'books.json')
    df = spark.read.json(books_path)
    print(f"Total rows: {count_rows(df)}")
    print(f"Total distinct rows: {count_distinct_rows(df)}")
    df_drop_dup = drop_duplicates(df)
    df_drop_dup.show(10, truncate=False)
    df_1 = assign_flag_column(df,"title","ODD HOURS","newHours")
    df_1.show(10, truncate=False)
    check_contain(df_1,"title","THE","universal").show(5, truncate=False)
    substring_col(df_1, "author", 1, 3, "newTitle1").show(5, truncate=False)
    substring_col(df_1, "author", 3, 6, "newTitle2").show(5, truncate=False)
    show_and_count_columns(df_1, ["title", "author", "rank", "price"])
    start_with(df_1, "title", "THE", ["author", "title"]).show(5, truncate=False)
    end_with(df_1, "title", "IN", ["author", "title"]).show(5, truncate=False)
    drop_cols(df, ["publisher", "published_date"]).show(5, truncate=False)
    group_and_count(df, "author", "book_count").show(10, truncate=False)
    filter_col(df, [("title", '==', "THE HOST")]).show(5, truncate=False)