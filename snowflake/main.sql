select * from BOOTCAMP.TEST.CUSTOMER;

list @bootcamp.test.S3_STAGE;

create table BOOTCAMP.TEST.data(id int, name string);

copy into data from @S3_STAGE/data/data.csv
FILE_FORMAT=(TYPE= 'CSV')
PATTERN= '.*.csv';


select * from data;

CREATE table data1(id int, name string);

-- Loads all files to this table
-- If there are previous files loaded, it keeps metadata so it doesn't reload those again - incremental data loading
copy into data1 from @S3_STAGE/data
FILE_FORMAT=(TYPE= 'CSV')
PATTERN= '.*.csv';

select * from data1;



create or replace table LISTING(PARQUET_RAW VARIANT)

copy into LISTING from (SELECT $1 from  @S3_STAGE/redshift_output/listings_parquet) 
FILE_FORMAT=(TYPE= 'PARQUET')
PATTERN= '.*.parquet';

select $1:dateid, $1:eventid from listing;


create table listing_parquet(
    listid integer,
    sellerid integer,
    eventid integer,
    dateid smallint,
    numtickets smallint,
    priceperticket decimal(8,2),
    totalprice decimal(8,2),
    listtime timestamp);


copy into listing_parquet from (SELECT $1:listid, $1:sellerid,$1:eventid, $1:dateid,$1:numtickets, $1:priceperticket,$1:totalprice, $1:listtime from  @S3_STAGE/redshift_output/listings_parquet) 
FILE_FORMAT=(TYPE= 'PARQUET')
PATTERN= '.*.parquet';

SELECT * from listing_parquet;


copy into @S3_STAGE/snowflake_unload/temp1/ from LISTING;

create table location(country string, state string, city string);

insert into location 
values('IND','MP','INDORE'),('IND','MP','BHOPAL'),('IND','UP','NOIDA'),('IND','UP','GZB'),('IND','KN','BANGLURU'),('IND','KN','MYSORE');

select * from location;

update location
set country='INDIA'

select * from location;

-- Offset before 2 min
select * from location at (OFFSET => -60 * 2)