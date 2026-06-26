try:
    from student_project.utilities.project_helper import *
except:
    from utilities.project_helper import *

def bronze_silver(spark):
    global_path = "file:///home/takeo/pycharmproject/data"

    # Read CSV
    bronze_customers = bronze_ingestion(spark, f"{global_path}/customers.csv", "customers")
    bronze_products = bronze_ingestion(spark, f"{global_path}/products.csv", "products")
    bronze_stores = bronze_ingestion(spark, f"{global_path}/stores.csv", "stores")
    bronze_sales = bronze_ingestion(spark, f"{global_path}/sales.csv", "sales")

    # Fix data type and partition by sales date
    silver_sales = silver_sales_transform_partition(spark, bronze_sales, store_table_name="silver_sales",
                                                    partition_column="sale_date",
                                                    file_format="parquet",
                                                    transformation_column={"sale_id": "int", "product_id": "int",
                                                                           "customer_id": "int",
                                                                           "store_id": "int", "quantity": "int",
                                                                           "sale_date": "date"})

    silver_customers = silver_sales_transform(spark, bronze_customers, store_table_name="silver_customers",
                                              file_format="parquet",
                                              transformation_column={"customer_id": "int", "customer_name": "string",
                                                                     "city": "string", "state": "string"})

    silver_products = silver_sales_transform(spark, bronze_products, store_table_name="silver_products", file_format="parquet",
                                             transformation_column={"product_id": "int", "product_name": "string",
                                                                    "category": "string", "unit_price": "double"})

    silver_stores = silver_sales_transform(spark, bronze_stores, store_table_name="silver_stores", file_format="parquet",
                                           transformation_column={"store_id": "int", "store_name": "string",
                                                                  "city": "string", "state": "string"})
