CREATE SCHEMA test;

create table test.listing(
	listid integer not null distkey,
	sellerid integer not null,
	eventid integer not null,
	dateid smallint not null  sortkey,
	numtickets smallint not null,
	priceperticket decimal(8,2),
	totalprice decimal(8,2),
	listtime timestamp);

copy test.listing 
from 's3://sunil1ebucket/redshift_input/listings_pipe.txt' 
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>';

select * from test.listing;

unload ('select * from test.listing')
to 's3://sunil1ebucket/redshift_output/listings_txt/file'
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>';

unload ('select * from test.listing')
to 's3://sunil1ebucket/redshift_output/listings_parquet/file'
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
PARQUET;


unload ('select * from test.listing')
to 's3://sunil1ebucket/redshift_output/listings_csv/file'
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
CSV;

create table test.listing_parquet(
	listid integer not null distkey,
	sellerid integer not null,
	eventid integer not null,
	dateid smallint not null  sortkey,
	numtickets smallint not null,
	priceperticket decimal(8,2),
	totalprice decimal(8,2),
	listtime timestamp);

copy test.listing_parquet 
from 's3://sunil1ebucket/redshift_output/listings_parquet/file'
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
format as parquet;


select * from test.listing_parquet;


create table test.event(
	eventid integer not null distkey,
	venueid smallint not null,
	catid smallint not null,
	dateid smallint not null sortkey,
	eventname varchar(200),
	starttime timestamp);

copy test.event
from 's3://sunil1ebucket/redshift_input/allevents_pipe.txt' 
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
removequotes
emptyasnull
blanksasnull
maxerror 5
delimiter '|'
timeformat 'YYYY-MM-DD HH:MI:SS';


create table test.venue_new(
venueid smallint not null,
venuename varchar(100) not null,
venuecity varchar(30),
venuestate char(2),
venueseats integer not null default '1000');

copy test.venue_new(venueid, venuename, venuecity, venuestate) 
from 's3://sunil1ebucket/redshift_input/venue_noseats.txt' 
iam_role 'arn:aws:iam::<ACCOUNT_ID>:role/<RedshiftCopyRole>'
delimiter '|';

select * from test.venue_new;

select * from test.employee;

CREATE SCHEMA IF NOT EXISTS covid_gold;

drop table covid_gold.fact_testing_state_daily;

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


-- ---- REDSHIFT COPY ----
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

SELECT s.state_name, f.new_cases
FROM covid_gold.fact_cases_state_daily f
JOIN covid_gold.dim_state s ON s.state_code = f.state_code
WHERE f.date_id = 20200515
ORDER BY f.new_cases DESC
LIMIT 5;


select * from covid_gold.fact_cases_state_daily
where date_id LIKE '202005%';


-- Compute daily positivity; if you want a 7-day average, wrap with a window or pre-aggregate
SELECT d.full_date,
       (t.tests_pos_cum::double precision / NULLIF(t.tests_total_cum, 0)) AS positivity_rate
FROM covid_gold.fact_testing_state_daily t
JOIN covid_gold.dim_date d   ON d.date_id = t.date_id
WHERE t.state_code = 'NY'
ORDER BY d.full_date;


SELECT d.full_date,
       c.new_cases,
       t.new_tests,
       (t.tests_pos_cum::double precision / NULLIF(t.tests_total_cum, 0)) AS positivity_rate
FROM covid_gold.fact_cases_state_daily   c
JOIN covid_gold.fact_testing_state_daily t
  ON t.date_id = c.date_id AND t.state_code = c.state_code
JOIN covid_gold.dim_date d ON d.date_id = c.date_id
WHERE c.state_code = 'CA'
ORDER BY d.full_date;