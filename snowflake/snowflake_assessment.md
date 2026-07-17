1. i. 
CREATE DATABASE IF NOT EXISTS bootcamp;
USE DATABASE bootcamp;

CREATE SCHEMA IF NOT EXISTS snow;
USE SCHEMA snow;

create table Employee (
    EMPLOYEE_ID INT, 
    NAME VARCHAR(50),
    SALARY INT,
    DEPARTMENT_ID INT, 
    JOINING_DATE DATE
)

copy into EMPLOYEE from @S3_STAGE/data/employee.csv
FILE_FORMAT=(TYPE= 'CSV')
PATTERN= '.*.csv';


1. ii. 
COPY INTO @S3_STAGE_ASSESSMENT/employee_output/Employee_
FROM EMPLOYEE
FILE_FORMAT = (
    TYPE = CSV
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    HEADER = TRUE
)
OVERWRITE = TRUE;

2. i.
unload ('select * from test.listing')
to 's3://sunil1ebucket/staging_output/listing_data'
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
FORMAT AS PARQUET
ALLOWOVERWRITE;


2. ii.
create table listing_parquet(
    listid integer,
    sellerid integer,
    eventid integer,
    dateid smallint,
    numtickets smallint,
    priceperticket decimal(8,2),
    totalprice decimal(8,2),
    listtime timestamp);


copy into listing_parquet from (SELECT $1:listid, $1:sellerid,$1:eventid, $1:dateid,$1:numtickets, $1:priceperticket,$1:totalprice, $1:listtime from  @S3_STAGE_ASSESSMENT/staging_output) 
FILE_FORMAT=(TYPE= 'PARQUET')
PATTERN= '.*.parquet';

select * from listing_parquet;