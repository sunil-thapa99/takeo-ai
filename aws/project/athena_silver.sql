-- ---- ATHENA (SILVER) ----
CREATE DATABASE IF NOT EXISTS covid_silver_db;

-- Cases
CREATE EXTERNAL TABLE IF NOT EXISTS covid_silver_db.cases_standardized (
    full_date date,
    state_name string,
    cases_cum bigint,
    deaths_cum bigint
)
PARTITIONED BY (
    state_code string,
    year int,
    month int,
    day int
)
STORED AS PARQUET
LOCATION 's3://aws-takeo-covid-project/covid/silver/cases_standardized/';

MSCK REPAIR TABLE covid_silver_db.cases_standardized;

-- Testing
CREATE EXTERNAL TABLE IF NOT EXISTS covid_silver_db.testing_standardized (
  full_date date,
  state_name string,
  tests_total_cum bigint,
  tests_pos_cum bigint,
  tests_neg_cum bigint
)
PARTITIONED BY (state_code string, year int, month int, day int)
STORED AS PARQUET
LOCATION 's3://aws-takeo-covid-project/covid/silver/testing_standardized/';

MSCK REPAIR TABLE covid_silver_db.testing_standardized;

-- QUICK QA
SELECT MIN(full_date), MAX(full_date), COUNT(*) FROM covid_silver_db.cases_standardized;
SELECT state_code, COUNT(*) FROM covid_silver_db.testing_standardized GROUP BY 1 ORDER BY 2 DESC;


