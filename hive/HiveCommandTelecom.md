CREATE EXTERNAL TABLE call_data_ext (
    call_id INT,
    customer_id INT,
    call_duration FLOAT,
    region STRING,
    call_date DATE  
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INPATH '/home/takeo/call_data.csv' INTO TABLE call_data_ext;


CREATE EXTERNAL TABLE data_usage_ext (
    usage_id INT,
    customer_id INT,
    data_used FLOAT,
    region STRING,
    usage_date DATE  
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INPATH '/home/takeo/data_usage.csv' INTO TABLE data_usage_ext;

CREATE EXTERNAL TABLE sms_data_ext (
    sms_id INT,
    customer_id INT,
    sms_count INT,
    region STRING,
    sms_date DATE  
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INPATH '/home/takeo/sms_data.csv' INTO TABLE sms_data_ext;


CREATE TABLE call_data (
    call_id INT,
    customer_id INT,
    call_duration FLOAT
)
PARTITIONED BY (call_date STRING, region STRING)
CLUSTERED BY (customer_id) INTO 10 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC;

SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE call_data
PARTITION (call_date, region)
SELECT 
    call_id,
    customer_id,
    call_duration,
    call_date,
    region
FROM call_data_ext;



CREATE TABLE data_usage (
    usage_id INT,
    customer_id INT,
    data_used FLOAT
)
PARTITIONED BY (usage_date STRING, region STRING)
CLUSTERED BY (customer_id) INTO 10 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC;

SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE data_usage
PARTITION (usage_date, region)
SELECT 
    usage_id,
    customer_id,
    data_used,
    usage_date,
    region
FROM data_usage_ext;



CREATE TABLE sms_data (
    sms_id INT,
    customer_id INT,
    sms_count FLOAT
)
PARTITIONED BY (sms_date STRING, region STRING)
CLUSTERED BY (customer_id) INTO 10 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC;

SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE sms_data
PARTITION (sms_date, region)
SELECT 
    sms_id,
    customer_id,
    sms_count,
    sms_date,
    region
FROM sms_data_ext;