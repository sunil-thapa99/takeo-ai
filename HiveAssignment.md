<!-- Section 1 -->

<!-- Create database hive_test -->
CREATE DATABASE hive_test;
USE hive_test;

<!-- Create table statement -->
CREATE TABLE salesman (
    salesman_id INT,
    name STRING,
    city STRING,
    commission DOUBLE    
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

CREATE TABLE customer (
    customer_id INT,
    cust_name STRING,
    city STRING,
    grade INT,
    salesman_id INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

CREATE TABLE orders (
    ord_no INT,
    purch_amt DOUBLE,
    ord_date DATE,
    customer_id INT,
    salesman_id INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

load data local inpath '/home/takeo/salesman.csv' into table salesman;

load data local inpath '/home/takeo/customer.csv' into table customer;

load data local inpath '/home/takeo/order.csv' into table orders;


<!-- Write a SQL statement to prepare a list with salesman name, customer name, and their cities for the salesmen and customer who belongs to the same city. -->
select s.name as salesman_name, c.cust_name as customer_name, s.city as city from salesman s join customer c on s.city=c.city;

<!-- Write a SQL statement to know which salesman are working for which customer. -->
select s.name as salesman_name, c.cust_name as customer_name from salesman s join customer c on s.salesman_id=c.salesman_id;

<!-- Write a SQL statement to make a list with order no, purchase amount, customer name and their cities for those orders which order amount between 500 and 2000. -->
select o.ord_no, o.purch_amt, c.cust_name, c.city from orders o join customer c on o.customer_id = c.customer_id where o.purch_amt between 500 and 2000;

<!-- Write a SQL statement to find the list of customers who appointed a salesman for their jobs who gets a commission from the company is more than 12%. -->
select c.cust_name, s.name as salesman_name, s.commission from customer c join salesman s on c.salesman_id = s.salesman_id where s.commission > 0.12;

<!-- Write a SQL statement to find the list of customers who appointed a salesman for their jobs who does not live in the same city where their customer lives, and gets a commission above 12% . -->
select s.name as salesman_name, c.cust_name, s.city as salesman_city, s.commission, c.city as customer_city from customer c join salesman s on c.salesman_id = s.salesman_id where s.commission > 0.12 and s.city <> c.city;


<!-- Section 2 -->

<!-- Query 1: Create table with complex data -->
create table salesdetail_complex (Product_ID INT,productdetails map<String,String>,Order_Priority VARCHAR(4),merchantType CHAR(4),Sale_Amount DOUBLE,Order_Quantity BIGINT,Discount FLOAT,Salaryhike TINYINT,companyprofit SMALLINT, financeDeficit DECIMAL(8,2),indian BOOLEAN,saledate array<date>,saleyear array<int>,selleramountfile array<DOUBLE>,orderQuantityfile array<BIGINT>,costlist map<int,int>,strutureType struct<city:string,state:string,pin:bigint>,systemdatetime array<String>) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' collection items terminated by '$' map keys terminated by '#';

nano salesdetail.txt

load data local inpath '/home/takeo/salesdetail.txt' into table salesdetail_complex;

<!-- Query 2: view 2 records -->
select * from salesdetail_complex limit 2;


<!-- Query 3: Non partition table -->
CREATE TABLE non_part (
    dateid SMALLINT,
    caldate DATE,
    day STRING,
    week SMALLINT,
    month STRING,
    qtr STRING,
    year SMALLINT,
    holiday BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;

load data local inpath '/home/takeo/non_part.txt' into table non_part;

<!-- Query 4: Partition table on caldate, load from non partition -->
CREATE TABLE date_part (
    dateid SMALLINT,
    day STRING,
    week SMALLINT,
    month STRING,
    qtr STRING,
    year SMALLINT,
    holiday BOOLEAN
)
PARTITIONED BY (
    caldate DATE
)
STORED AS TEXTFILE;

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT INTO TABLE date_part
PARTITION (caldate)
SELECT
    dateid,
    day,
    week,
    month,
    qtr,
    year,
    holiday,
    caldate
FROM non_part;

show partitions date_part;

<!-- Query 5: Create a partitioned and bucketed table -->
CREATE TABLE date_part_bucket (
    dateid SMALLINT,
    day STRING,
    week SMALLINT,
    month STRING,
    qtr STRING,
    year SMALLINT,
    holiday BOOLEAN
)
PARTITIONED BY (
    caldate DATE
)
CLUSTERED BY (dateid)
INTO 4 BUCKETS
STORED AS ORC;

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

SET hive.enforce.bucketing=true;

INSERT INTO TABLE date_part_bucket
PARTITION (caldate)
SELECT
    dateid,
    day,
    week,
    month,
    qtr,
    year,
    holiday,
    caldate
FROM non_part;

SELECT * FROM date_part_bucket LIMIT 5;