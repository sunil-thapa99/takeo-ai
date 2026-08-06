# Capstone — Health Insurance Data Pipeline

PySpark ETL pipeline that reads raw health-insurance data from **S3**, cleanses it, and loads it into **Amazon Redshift**.

## Flow

```
S3 (raw JSON/CSV)  →  PySpark cleansing  →  Redshift (cleaned_data schema)
```

## Layout

```
src/
  cleansing/        one script per entity (claims, patients, subscribers, groups, ...)
  utils/
    spark_sessions.py   Spark session + Redshift read/write helpers
    utils.py            shared cleaning helpers (dedupe, fillna, schema, lowercase)
  AWS Commands/
    Redshift.sql        schema + table DDL
docs/                 requirements & design documents
jira/                 project tickets
requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

Set credentials in `.env` (S3 access + Redshift login):

```
ACCESS_KEY=...
SECRET_KEY=...
USERNAME=...
PASSWORD=...
```

## Run

Create the Redshift schema/tables first (run `src/AWS Commands/Redshift.sql`), then submit any cleansing job:

```bash
spark-submit \
  --jars ~/redshift-jdbc42-2.1.0.9.jar \
  --packages org.apache.hadoop:hadoop-aws:3.3.4 \
  src/cleansing/claims_cleanse.py
```

Each script in `src/cleansing/` runs the same way — swap the filename.

## Note

`.env` currently holds live AWS keys. Rotate them and keep the file out of version control (`.gitignore`).
