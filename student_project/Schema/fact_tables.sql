CREATE TABLE fact_sales (
    sale_id INT,
    customer_id INT,
    product_id INT,
    store_id INT,
    date_key DATE,
    quantity INT,
    total_amount INT
)
PARTITIONED BY (date_key)
STORED AS PARQUET;
