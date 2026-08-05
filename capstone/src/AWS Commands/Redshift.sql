CREATE SCHEMA cleaned_data;
CREATE SCHEMA "Project-Output";

-- Create table: cleaned_data
CREATE TABLE IF NOT EXISTS cleaned_data.hospitals (
    hospital_id VARCHAR(50) NOT NULL PRIMARY KEY,
    hospital_name VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100)
) DISTSTYLE ALL
SORTKEY(hospital_id);

CREATE TABLE IF NOT EXISTS cleaned_data.group_subgroup (
    group_id VARCHAR(50) NOT NULL,
    group_name VARCHAR(100),
    subgroup_id VARCHAR(50) NOT NULL,
    subgroup_name VARCHAR(100),
    policy_type VARCHAR(50),
    premium_rate DECIMAL(10,2),
    PRIMARY KEY (group_id, subgroup_id)
) DISTSTYLE ALL
SORTKEY(group_id, subgroup_id);

CREATE TABLE IF NOT EXISTS cleaned_data.patients (
    patient_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    gender CHAR(1),
    city VARCHAR(100),
    diagnosis VARCHAR(200),
    admission_date DATE,
    discharge_date DATE,
    hospital_id VARCHAR(50) REFERENCES cleaned_data.hospitals(hospital_id),
    insurance_type VARCHAR(50),
    total_charges DECIMAL(12,2),
    procedure_name VARCHAR(200)
) DISTKEY(patient_id)
SORTKEY(patient_id);

CREATE TABLE IF NOT EXISTS cleaned_data.subscribers (
    subscriber_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    gender CHAR(1),
    city VARCHAR(100),
    group_id VARCHAR(50),
    subgroup_id VARCHAR(50),
    policy_type VARCHAR(50),
    monthly_premium DECIMAL(10,2),
    enrollment_date DATE,
    FOREIGN KEY (group_id, subgroup_id)
    REFERENCES cleaned_data.group_subgroup(group_id, subgroup_id)
) DISTKEY(subscriber_id)
SORTKEY(subscriber_id);

CREATE TABLE IF NOT EXISTS cleaned_data.claims (
    claim_id VARCHAR(50) NOT NULL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES cleaned_data.patients(patient_id),
    subscriber_id VARCHAR(50) REFERENCES cleaned_data.subscribers(subscriber_id),
    claim_date DATE,
    disease VARCHAR(200),
    claim_amount DECIMAL(12,2),
    status VARCHAR(50),
    city VARCHAR(100)
) DISTKEY(claim_id)
SORTKEY(claim_id);

-- Product-Output
CREATE TABLE IF NOT EXISTS "Project-Output".uc01_max_claims_disease
 (disease VARCHAR(200), claim_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc02_subscribers_under30
 (subscriber_id VARCHAR(50), name VARCHAR(100), age INTEGER, subgroup_id
VARCHAR(50));

CREATE TABLE IF NOT EXISTS "Project-Output".uc03_group_max_subgroups
 (group_id VARCHAR(50), group_name VARCHAR(100), subgroup_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc04_hospital_most_patients
 (hospital_id VARCHAR(50), hospital_name VARCHAR(200), patient_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc05_most_subscribed_subgroup
 (subgroup_id VARCHAR(50), subgroup_name VARCHAR(100), subscription_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc06_total_rejected_claims
 (total_rejected BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc07_city_most_claims
 (city VARCHAR(100), claim_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc08_govt_vs_private
 (policy_type VARCHAR(50), subscriber_count BIGINT);

CREATE TABLE IF NOT EXISTS "Project-Output".uc09_avg_monthly_premium
 (avg_monthly_premium DECIMAL(10,2));

CREATE TABLE IF NOT EXISTS "Project-Output".uc10_most_profitable_group
 (group_id VARCHAR(50), group_name VARCHAR(100), total_profit DECIMAL(14,2));

CREATE TABLE IF NOT EXISTS "Project-Output".uc11_patients_under18_cancer
 (patient_id VARCHAR(50), name VARCHAR(100), age INTEGER, diagnosis VARCHAR(200));

CREATE TABLE IF NOT EXISTS "Project-Output".uc12_cashless_high_charges
 (patient_id VARCHAR(50), name VARCHAR(100), insurance_type VARCHAR(50),
total_charges DECIMAL(12,2));

CREATE TABLE IF NOT EXISTS "Project-Output".uc13_female_knee_surgery
 (patient_id VARCHAR(50), name VARCHAR(100), age INTEGER, gender CHAR(1),
 procedure_name VARCHAR(200), admission_date DATE);