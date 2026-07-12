-- ---- ATHENA (GOLD) ----
CREATE DATABASE IF NOT EXISTS covid_gold_db;

CREATE EXTERNAL TABLE IF NOT EXISTS covid_gold_db.dim_date (
    full_date date,
    date_id int PRIMARY KEY,
    year int,
    month int,
    day int,
    dow int,
    is_weekend boolean
)
STORED AS PARQUET
LOCATION 's3://aws-takeo-covid-project/covid/gold/dim_date/';

CREATE EXTERNAL TABLE IF NOT EXISTS covid_gold_db.dim_state (
  state_code string,
  state_name string
)
STORED AS PARQUET
LOCATION 's3://aws-takeo-covid-project/covid/gold/dim_state/';

CREATE EXTERNAL TABLE IF NOT EXISTS covid_gold_db.fact_cases_state_daily (
  date_id int,
  cases_cum bigint,
  deaths_cum bigint,
  new_cases int,
  new_deaths int
)
PARTITIONED BY (state_code string)
STORED AS PARQUET
LOCATION 's3://aws-takeo-covid-project/covid/gold/fact_cases_state_daily/';
MSCK REPAIR TABLE covid_gold_db.fact_cases_state_daily;

CREATE EXTERNAL TABLE IF NOT EXISTS covid_gold_db.fact_testing_state_daily (
  date_id int,
  tests_total_cum bigint,
  tests_pos_cum bigint,
  tests_neg_cum bigint,
  new_tests int,
  positivity_rate double
)
PARTITIONED BY (state_code string)
STORED AS PARQUET
LOCATION 's3://aws-takeo-covid-project/covid/gold/fact_testing_state_daily/';
MSCK REPAIR TABLE covid_gold_db.fact_testing_state_daily;


