from pyspark.sql.functions import col

def load_fact_sales(spark):
    sales = spark.table("silver_sales")
    products = spark.table("silver_products")

    fact_df = (
        sales.join(products, "product_id")
             .withColumn("total_amount", col("quantity") * col("unit_price"))
             .select(
                 "sale_id",
                 "customer_id",
                 "product_id",
                 "store_id",
                 col("sale_date").alias("date_key"),
                 "quantity",
                 "total_amount"
             )
    )

    (
        fact_df.write
        .mode("overwrite")
        .partitionBy("date_key")
        .format("parquet")
        .saveAsTable("iphone_analytics.fact_sales")
    )


def load_fact_customer(spark):
    customers = spark.table("silver_customers")
    fact_df = (
        customers.select("customer_id", "customer_name", "city", "state")
    )
    fact_df.write.mode("overwrite").format("parquet").saveAsTable("iphone_analytics.fact_customers")

def load_fact_store(spark):
    stores = spark.table("silver_stores")
    fact_df = (
        stores.select("store_id", "store_name", "city", "state")
    )
    fact_df.write.mode("overwrite").format("parquet").saveAsTable("iphone_analytics.fact_stores")

def load_fact_product(spark):
    products = spark.table("silver_products")
    fact_df = (
        products.select("product_id", "product_name", "category", "unit_price")
    )
    fact_df.write.mode("overwrite").format("parquet").saveAsTable("iphone_analytics.fact_products")