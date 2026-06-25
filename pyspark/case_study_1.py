'''
Scenario:

You have a dataset of e-commerce transactions, and you want to analyze customer purchase patterns, total spending, product preferences, and various other insights using PySpark DataFrame operations and SQL queries. The dataset contains the following columns:
- transaction_id: Unique ID for each transaction
- customer_id: Unique ID for each customer
- product_id: Unique ID for each product
- product_name: Name of the product
- category: Category of the product
- price: Price of the product
- quantity: Quantity purchased
This case study will demonstrate the use of common PySpark DataFrame transformations and actions, as well as SQL queries.
'''
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql import SparkSession

def main(df):
    # Using Filter Transformation
    df_filtered = df.filter(df.quantity > 1)

    # Handling null values
    average_price = df.selectExpr(("avg(price)")).collect()[0][0]
    df_filled = df.na.fill({"price": average_price})

    # Dropping Duplicates
    df_no_duplicates = df.dropDuplicates(["customer_id", "product_id"])

    # Selecting Specific Columns
    df_selected = df.select("customer_id", "product_name", "price", "quantity")

    # Grouping and aggregating data
    df_grouped = df.groupBy("customer_id").agg({"price": "sum"})

    # Joining Dataframes
    customer_data = [
        (101, "John Doe", "john@example.com"),
        (102, "Jane Smith", "jane@example.com"),
        (103, "Alice Johnson", "alice@example.com")
    ]
    customer_columns = ["customer_id", "customer_name", "email"]
    df_customers = spark.createDataFrame(customer_data, customer_columns)
    df_joined = df.join(df_customers, on="customer_id", how="inner")

    # Union of two dataframe
    new_data = [
        (6, 104, 5006, "Table", "Furniture", 200.0, 1)
    ]
    columns = ["transaction_id", "customer_id", "product_id", "product_name", "category", "price", "quantity"]
    df_new = spark.createDataFrame(new_data, columns)
    df_union = df.union(df_new)

    # Creating Temporary views using SQL
    df.createOrReplaceTempView("transactions")
    sql_results = spark.sql("SELECT customer_id, SUM(price*quantity) as total_spent FROM transactions GROUP BY customer_id")



if __name__ == "__main__":
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    file_path = 'file:///home/takeo/pycharmproject/sample_product.csv'
    colums = StructType([
        StructField("transaction_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("product_name", StringType(), True),
        StructField("category", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("quantity", DoubleType(), True),
    ])

    df = spark.read.option("header", False).schema(colums).csv(file_path)

    main(df)



