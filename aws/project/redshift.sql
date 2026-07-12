-- ---- REDSHIFT DDL ----
CREATE SCHEMA IF NOT EXISTS covid_gold;


CREATE TABLE IF NOT EXISTS covid_gold.dim_date (
  full_date date,
  date_id int PRIMARY KEY,
  year int,
  month int,
  day int,
  dow int,
  is_weekend boolean
) SORTKEY(date_id);

CREATE TABLE IF NOT EXISTS covid_gold.dim_state (
  state_code varchar(2) PRIMARY KEY,
  state_name varchar(64)
) DISTSTYLE ALL;

CREATE TABLE IF NOT EXISTS covid_gold.fact_cases_state_daily (
  date_id int NOT NULL REFERENCES covid_gold.dim_date(date_id),
  state_code varchar(2) NOT NULL REFERENCES covid_gold.dim_state(state_code),
  cases_cum bigint,
  deaths_cum bigint,
  new_cases bigint,
  new_deaths bigint
) DISTKEY(state_code) SORTKEY(date_id, state_code);

CREATE TABLE IF NOT EXISTS covid_gold.fact_testing_state_daily (
  date_id int NOT NULL REFERENCES covid_gold.dim_date(date_id),
  state_code varchar(2) NOT NULL REFERENCES covid_gold.dim_state(state_code),
  tests_total_cum bigint,
  tests_pos_cum bigint,
  tests_neg_cum bigint,
  new_tests bigint,
  positivity_rate double precision
) DISTKEY(state_code) SORTKEY(date_id, state_code);



-- Copy from s3 (Gold parquet to redshift)
-- ---- REDSHIFT COPY ----
-- Replace with your role ARN and bucket
COPY covid_gold.dim_date
FROM 's3://aws-takeo-covid-project/covid/gold/dim_date/'
IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
FORMAT AS PARQUET;

COPY covid_gold.dim_state
FROM 's3://aws-takeo-covid-project/covid/gold/dim_state/'
IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
FORMAT AS PARQUET;

COPY covid_gold.fact_cases_state_daily
FROM 's3://aws-takeo-covid-project/covid/gold/fact_cases_state_daily/'
IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
FORMAT AS PARQUET;

COPY covid_gold.fact_testing_state_daily
FROM 's3://aws-takeo-covid-project/covid/gold/fact_testing_state_daily/'
IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
FORMAT AS PARQUET;

ANALYZE VERBOSE;


