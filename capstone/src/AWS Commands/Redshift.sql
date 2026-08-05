CREATE SCHEMA cleaned_data;
CREATE SCHEMA "Project-Output";

-- Create table: cleaned_data
CREATE TABLE IF NOT EXISTS cleaned_data.patients (
    patient_id VARCHAR(50) NOT NULL PRIMARY KEY,
    patient_name VARCHAR(100),
    patient_gender VARCHAR(10),
    patient_birth_date DATE,
    patient_phone VARCHAR(20),
    disease_name VARCHAR(200),
    city VARCHAR(100),
    hospital_id VARCHAR(50)
) DISTKEY(patient_id) SORTKEY(patient_id);

CREATE TABLE IF NOT EXISTS cleaned_data.claims (
    claim_id INTEGER NOT NULL PRIMARY KEY,
    patient_id VARCHAR(50),
    disease_name VARCHAR(200),
    sub_id VARCHAR(50),
    claim_or_rejected VARCHAR(5),
    claim_type VARCHAR(50),
    claim_amount DECIMAL(12,2),
    claim_date DATE
) DISTKEY(claim_id) SORTKEY(claim_id);

CREATE TABLE IF NOT EXISTS cleaned_data.subscribers (
    sub_id VARCHAR(50) NOT NULL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    country VARCHAR(50),
    city VARCHAR(100),
    zip_code VARCHAR(20),
    subgrp_id VARCHAR(10),
    elig_ind VARCHAR(5),
    eff_date DATE,
    term_date DATE
) DISTKEY(sub_id) SORTKEY(sub_id);

CREATE TABLE IF NOT EXISTS cleaned_data.groups (
    grp_id VARCHAR(10) NOT NULL PRIMARY KEY,
    grp_name VARCHAR(200),
    grp_type VARCHAR(20),
    country VARCHAR(50),
    premium_written DECIMAL(12,2),
    zipcode VARCHAR(20),
    city VARCHAR(100),
    group_year INTEGER
) DISTSTYLE ALL SORTKEY(grp_id);

CREATE TABLE IF NOT EXISTS cleaned_data.subgroups (
    subgrp_id VARCHAR(10) NOT NULL PRIMARY KEY,
    subgrp_name VARCHAR(100),
    monthly_premium DECIMAL(10,2)
) DISTSTYLE ALL;

CREATE TABLE IF NOT EXISTS cleaned_data.grpsubgrp (
    subgrp_id VARCHAR(10) NOT NULL,
    grp_id VARCHAR(10) NOT NULL,
    PRIMARY KEY (subgrp_id, grp_id)
) DISTSTYLE ALL;

CREATE TABLE IF NOT EXISTS cleaned_data.hospitals (
    hospital_id VARCHAR(10) NOT NULL PRIMARY KEY,
    hospital_name VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(50)
) DISTSTYLE ALL;

CREATE TABLE IF NOT EXISTS cleaned_data.disease (
 subgrp_id VARCHAR(10),
 disease_id VARCHAR(10),
 disease_name VARCHAR(200),
 PRIMARY KEY (disease_id)
) DISTSTYLE ALL;

-- Product-Output
CREATE TABLE IF NOT EXISTS "Project-Output".uc01_max_claims_disease
 (disease_name VARCHAR(200), claim_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc02_subscribers_under30
 (sub_id VARCHAR(50), first_name VARCHAR(100), last_name VARCHAR(100), age
INTEGER, subgrp_id VARCHAR(10));

CREATE TABLE IF NOT EXISTS "Project-Output".uc03_group_max_subgroups
 (grp_id VARCHAR(10), grp_name VARCHAR(200), subgroup_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc04_hospital_most_patients
 (hospital_id VARCHAR(10), hospital_name VARCHAR(200), patient_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc05_most_subscribed_subgroup
 (subgrp_id VARCHAR(10), subgrp_name VARCHAR(100), subscription_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc06_total_rejected_claims
 (total_rejected BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc07_city_most_claims
 (city VARCHAR(100), claim_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc08_govt_vs_private
 (grp_type VARCHAR(20), subscriber_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc09_avg_monthly_premium
 (avg_monthly_premium DECIMAL(10,2));

CREATE TABLE IF NOT EXISTS "Project-Output".uc10_most_profitable_group
 (grp_id VARCHAR(10), grp_name VARCHAR(200), total_profit DECIMAL(14,2));

CREATE TABLE IF NOT EXISTS "Project-Output".uc11_patients_under18_cancer
 (patient_id VARCHAR(50), patient_name VARCHAR(100), age INTEGER, disease_name
VARCHAR(200));

CREATE TABLE IF NOT EXISTS "Project-Output".uc12_high_value_claims
 (claim_id INTEGER, patient_id VARCHAR(50), claim_type VARCHAR(50), claim_amount
DECIMAL(12,2));

CREATE TABLE IF NOT EXISTS "Project-Output".uc13_female_patients_over40
 (patient_id VARCHAR(50), patient_name VARCHAR(100), age INTEGER, patient_gender
VARCHAR(10), city VARCHAR(100));