<!-- June 10 - Ecommerce Assignment-->
<!-- Create External Table -->
CREATE EXTERNAL TABLE sales_data_ext (
    sale_id INT,
    product_id INT,
    product_category STRING,
    customer_id INT,
    sale_amount FLOAT,
    sale_date STRING,
    country STRING,
    region STRING
    
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/data/test/buss_case';

<!-- Remove file in hadoop -->
hadoop fs -rm /data/test/buss_case/customer.csv

set hive.exec.max.dynamic.partitions=10000;
set hive.exec.max.dynamic.partitions.pernode=10000;

<!-- Create partition data -->
CREATE TABLE sales_data (
    sale_id INT,
    product_id INT,
    product_category STRING,
    customer_id INT,
    sale_amount FLOAT,
    region STRING
)
PARTITIONED BY (sale_date STRING, country STRING);

<!-- Insert from non-partition to partition -->
set hive.exec.dynamic.partition.mode=nonstrict;
insert overwrite table sales_data partition(sale_date,country) 
select sale_id, product_id, product_category, customer_id, sale_amount, region, sale_date, country
from sales_data_ext;

<!-- Select query -->
SELECT SUM(sale_amount) AS total_sales
FROM sales_data
WHERE sale_date = '2023-08-01' AND country = 'US';

<!-- Top Products by category in a region -->
SELECT product_id, SUM(sale_amount) AS total_sales
FROM sales_data
WHERE product_category = 'Electronics' AND region = 'North America'
GROUP BY product_id
ORDER BY total_sales DESC
LIMIT 10;

<!-- Customer purchase trends -->
SELECT product_category, SUM(sale_amount) AS total_spent
FROM sales_data
WHERE customer_id = 12345
GROUP BY product_category
ORDER BY total_spent DESC;


