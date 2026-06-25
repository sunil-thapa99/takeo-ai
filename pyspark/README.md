# PySpark — Scripts Overview

All scripts in this folder use **Apache PySpark** and share the `utility.py` helper module. Run each script from the `pyspark/` directory so that `from utility import *` resolves correctly.

---

## `utility.py`

Shared helper library imported by most scripts in this folder. Provides reusable PySpark DataFrame operations so individual scripts stay concise.

| Function | Description |
|---|---|
| `select_col(df, fields)` | Select columns by name or index range |
| `count_rows(df)` | Count total rows |
| `count_distinct_rows(df)` | Count unique rows |
| `transform_col(df, col, new_col, type)` | Cast a column to a new type |
| `update_col(df, col, new_col, factor)` | Multiply a column by a number |
| `add_col(df, col, const)` | Add a column with a constant value |
| `drop_duplicates(df, cols=None)` | Drop duplicate rows globally or by column subset |
| `sort_dataframe(df, sort_specs)` | Sort by multiple columns asc/desc |
| `create_schema(columns_dict)` | Build a `StructType` schema from a `{name: Type}` dict |
| `agg_function(df, group_cols, agg_col, metrics)` | GroupBy + aggregate (count/min/max/avg/mean/sum) |
| `filter_col(df, conditions)` | Filter rows using `(col, op, value)` condition tuples |
| `assign_flag_column(df, col, val, new_col)` | Add a 0/1 flag column based on value match |
| `check_contain(df, col, val, new_col)` | Add boolean column for string containment |
| `substring_col(df, col, start, end, title)` | Extract a substring range from a column |
| `show_and_count_columns(df, cols)` | Show selected columns and print count |
| `start_with(df, col, val, cols)` | Filter rows where column starts with a value |
| `end_with(df, col, val, cols)` | Filter rows where column ends with a value |
| `drop_cols(df, cols)` | Drop one or more columns |
| `group_and_count(df, col, alias)` | GroupBy a column and count occurrences |
| `read(spark, format, path, ...)` | Read any file format into a DataFrame |
| `write(df, format, path)` | Write a DataFrame to any format (overwrite mode) |

---

## `pyspark_class.py` — Day 1: RDD Word Count

**Topic:** Introduction to Spark RDDs and word counting.

Reads a text file, splits it into words, maps each word to a `(word, 1)` pair, reduces by key to count occurrences, then saves the result.

> **Note:** Reads from `file:///home/takeo/test1.txt` (bootcamp server path). Update this path if running locally.

```bash
python pyspark_class.py
```

---

## `pyspark_day2.py` — Day 2: RDDs & DataFrame Creation

**Topics:** RDD transformations, converting RDDs to DataFrames, flat/nested StructType schemas.

- `wordCount()` — word count with keyword filtering (`wind`)
- `convertDF()` — create a DataFrame from an RDD using column names
- `structDF()` — create a DataFrame using a `StructType` schema, including nested structs

> **Note:** Reads from `file:///home/takeo/test1.txt` (bootcamp server path). Update this path if running locally.

```bash
python pyspark_day2.py
```

---

## `pyspark_day2_exercise.py` — Day 2 Exercise: Sales RDD Analysis

**Topics:** RDD map/filter/flatMap/reduceByKey/groupByKey/join.

Reads a sales CSV, parses each transaction, and produces:
- Total spending per customer (`reduceByKey`)
- List of products per customer (`groupByKey`)
- Products joined with a category lookup table (`join`)

> **Note:** Reads from `file:///home/takeo/sales.csv` (bootcamp server path — no local copy).

```bash
python pyspark_day2_exercise.py
```

---

## `pyspark_day3.py` — Day 3: DataFrame Column Operations

**Topics:** `select`, `withColumn`, type casting, column renaming, adding constant columns.

Defines helper functions:
- `selectCol()` — select flat or nested struct columns
- `transformCol()` — cast column type (e.g., salary to Double)
- `updateCol()` — multiply a column (e.g., salary × 50)
- `addCol()` — add a literal constant column

Demonstrates these on employee and car datasets.

```bash
python pyspark_day3.py
```

---

## `pyspark_day4_1.py` — Day 4 Part 1: Dropping Duplicates

**Topics:** `dropDuplicates()` on full rows and on column subsets.

Creates a small person dataset (Name, Age, Height) with duplicate rows, then:
1. Drops fully duplicate rows
2. Drops rows duplicated by `(Age, Height)` subset

Uses `utility.create_schema()` and `utility.drop_duplicates()`.

```bash
python pyspark_day4_1.py
```

---

## `pyspark_day4_2.py` — Day 4 Part 2: Aggregation & Filtering

**Topics:** GroupBy aggregation, filtering aggregated results, sorting.

Creates a city–temperature dataset and:
1. Aggregates average, sum, and count of temperature per city
2. Filters cities where total temperature > 30
3. Sorts results ascending by city name

Uses `utility.agg_function()`, `utility.filter_col()`, `utility.sort_dataframe()`.

```bash
python pyspark_day4_2.py
```

---

## `pyspark_day_5.py` — Day 5: Books JSON Analysis

**Topics:** Reading JSON, string functions, flag columns, substring, groupBy.

Reads `../data/books.json` and demonstrates a wide range of DataFrame operations:
- Count rows and distinct rows
- Drop duplicates
- Assign flag column (title != "ODD HOURS")
- String containment check (`THE`)
- Substring extraction from author name
- Filter by starts/ends-with
- Drop columns
- GroupBy author → book count
- Filter by exact title match

```bash
python pyspark_day_5.py
```

---

## `pyspark_day_6.py` — Day 6: CSV Read & Write

**Topics:** Reading and writing CSV files using the `utility.read()` / `utility.write()` helpers.

Reads `../data/zipcodes.csv`, displays the DataFrame, then writes it out as CSV to `/tmp/spark_output/zipcodes`.

```bash
python pyspark_day_6.py
```

---

## `pyspark_covid.py` — Project 6: COVID-19 Data Analysis

**Topics:** Real-world CSV analysis — grouping, aggregation, renaming, filtering, dropping columns.

Reads `../project6-Covid-19_data_analysis/CovidCases.csv` and:
1. Groups by `province` + `city`, computing sum/max of confirmed cases
2. Finds the top 2 provinces by total confirmed cases
3. Filters rows for Daegu province with >10 confirmed cases
4. Drops non-essential columns (`latitude`, `longitude`, `case_id`)

```bash
python pyspark_covid.py
```
