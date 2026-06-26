CREATE DATABASE IF NOT EXISTS iphone_analytics;
USE iphone_analytics;
-- dim_customer
CREATE TABLE dim_customer (
  customer_id INT,
  customer_name STRING,
  city STRING,
  state STRING
)
STORED AS PARQUET;

-- dim_product
CREATE TABLE dim_product (
  product_id INT,
  product_name STRING,
  category STRING,
  unit_price INT
)
STORED AS PARQUET;

-- dim_store
CREATE TABLE dim_store (
  store_id INT,
  store_name STRING,
  city STRING,
  state STRING
)
STORED AS PARQUET;

-- dim_date
CREATE TABLE dim_date (
  date_key DATE,
  year INT,
  month INT,
  day INT
)
STORED AS PARQUET;
