# iPhone Sales Analytics — PySpark ETL Pipeline

A PySpark-based ETL pipeline that processes iPhone sales data using a medallion architecture (Bronze → Silver → Gold) and stores the results in a Hive data warehouse with a star schema.

## Architecture

```
CSV Files  →  Bronze  →  Silver  →  Gold (Fact Tables)
              (raw)     (typed)     (analytics-ready)
```

The pipeline follows three layers:

| Layer | Description |
|---|---|
| **Bronze** | Raw CSV data ingested as-is into Parquet tables |
| **Silver** | Type-cast and cleaned data; sales partitioned by date |
| **Gold** | Fact and dimension tables ready for analytics queries |

## Project Structure

```
student_project/
├── main.py                          # Pipeline entry point
├── bronze_silver/
│   └── iphone_sales_project.py      # Bronze ingestion & Silver transformation
├── gold/
│   └── fact_load.py                 # Gold layer fact table loaders
├── utilities/
│   └── project_helper.py            # Shared helper functions
└── Schema/
    └── tables.sql                   # Hive DDL for the iphone_analytics database
```

## Data Model

**Database:** `iphone_analytics`

| Table | Type | Description |
|---|---|---|
| `fact_sales` | Fact | Sales transactions partitioned by `date_key` |
| `fact_customers` | Dimension | Customer details |
| `fact_products` | Dimension | Product catalog with pricing |
| `fact_stores` | Dimension | Store locations |

## Prerequisites

- Apache Spark with Hive support enabled
- Python 3.x
- PySpark
- Source CSV files (`customers.csv`, `products.csv`, `stores.csv`, `sales.csv`) at `/home/takeo/pycharmproject/data/`

## Running the Pipeline

```bash
spark-submit main.py
```

This will:
1. Ingest raw CSVs into Bronze Hive tables
2. Cast columns to correct types and write Silver tables (sales partitioned by `sale_date`)
3. Join and aggregate Silver tables into Gold fact tables

## Source Data

| File | Key Columns |
|---|---|
| `customers.csv` | `customer_id`, `customer_name`, `city`, `state` |
| `products.csv` | `product_id`, `product_name`, `category`, `unit_price` |
| `stores.csv` | `store_id`, `store_name`, `city`, `state` |
| `sales.csv` | `sale_id`, `customer_id`, `product_id`, `store_id`, `quantity`, `sale_date` |
