# Takeo Bootcamp — Code Repository

A collection of exercises, projects, and reference material from the Takeo Data Engineering Bootcamp. Topics span core Python, Apache Spark (PySpark), and Apache Hive.

---

## Folder Structure

```
.
├── python-assessment/      # Python fundamentals exercises (25 questions)
├── pyspark/                # PySpark scripts — day-by-day lessons + projects
├── hive/                   # Hive HQL commands, assignments, and class projects
├── notebooks/              # Jupyter notebooks for Python exercises
├── data/                   # Local data files (JSON, CSV)
├── project6-Covid-19_data_analysis/  # COVID-19 project data and spec
└── docs/                   # Assignment specs and case study documents
```

---

## Contents

### `python-assessment/`

| File | Description |
|---|---|
| [main.py](python-assessment/main.py) | 25 Python exercises covering strings, lists, dictionaries, loops, and interview questions |

See [python-assessment/README.md](python-assessment/README.md) for a full breakdown by question.

---

### `pyspark/`

All PySpark scripts share the `utility.py` helper module. Run scripts from the `pyspark/` directory.

| File | Day | Topic |
|---|---|---|
| [utility.py](pyspark/utility.py) | — | Shared reusable DataFrame helper functions |
| [pyspark_class.py](pyspark/pyspark_class.py) | Day 1 | RDD word count introduction |
| [pyspark_day2.py](pyspark/pyspark_day2.py) | Day 2 | RDD transformations & DataFrame creation |
| [pyspark_day2_exercise.py](pyspark/pyspark_day2_exercise.py) | Day 2 | Sales RDD analysis (map/filter/join) |
| [pyspark_day3.py](pyspark/pyspark_day3.py) | Day 3 | DataFrame column operations (select, cast, rename) |
| [pyspark_day4_1.py](pyspark/pyspark_day4_1.py) | Day 4 | Dropping duplicate rows and column subsets |
| [pyspark_day4_2.py](pyspark/pyspark_day4_2.py) | Day 4 | Aggregation, filtering, and sorting |
| [pyspark_day_5.py](pyspark/pyspark_day_5.py) | Day 5 | Books JSON analysis — string functions, flags, groupBy |
| [pyspark_day_6.py](pyspark/pyspark_day_6.py) | Day 6 | CSV read and write with utility helpers |
| [pyspark_covid.py](pyspark/pyspark_covid.py) | Project 6 | COVID-19 case data analysis |

See [pyspark/README.md](pyspark/README.md) for per-file details, function references, and run instructions.

---

### `hive/`

| File | Description |
|---|---|
| [HiveCommand.md](hive/HiveCommand.md) | Core HiveQL command reference |
| [HiveCommandTelecom.md](hive/HiveCommandTelecom.md) | Hive commands for telecom dataset |
| [HiveClassProject.md](hive/HiveClassProject.md) | Class project HQL queries |
| [HiveAssignment.md](hive/HiveAssignment.md) | Hive assignment questions and answers |
| [HiveAssignment.pdf](hive/HiveAssignment.pdf) | PDF version of the Hive assignment |

---

### `notebooks/`

Jupyter notebooks used for interactive Python exercises.

| File | Description |
|---|---|
| [June-03.ipynb](notebooks/June-03.ipynb) | Flatten nested lists, second largest, pairs summing to target |
| [June-04.ipynb](notebooks/June-04.ipynb) | Python exercises — June 4 session |
| [June-05.ipynb](notebooks/June-05.ipynb) | Python exercises — June 5 session |

---

### `data/`

Local data files used by PySpark scripts.

| File | Used By |
|---|---|
| `books.json` | `pyspark_day_5.py` |
| `books_1.json` | Reference / exploration |
| `zipcodes.csv` | `pyspark_day_6.py` |
| `simple-zipcodes.csv` | Reference / exploration |

---

### `project6-Covid-19_data_analysis/`

| File | Description |
|---|---|
| `CovidCases.csv` | Source dataset used by `pyspark/pyspark_covid.py` |
| `Spark-Class-Project-6-Covid-19 data analysis- No Grades.docx` | Project specification |

---

### `docs/`

| File | Description |
|---|---|
| `02-PySpark_DataFrame_Case_Study-DF1.docx` | DataFrame case study 2 specification |
| `03-Movie_Ratings_Case_Study-DF.docx` | Movie ratings case study specification |
| `Spark-Class-Project-5-Books_data_analysis.docx` | Books data analysis project specification |
| `setupPyspark.md` | PySpark local environment setup guide |

---

## Setup

See [docs/setupPyspark.md](docs/setupPyspark.md) for environment setup instructions.

### Quick Start

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pyspark

# Run a PySpark script (from the pyspark/ directory)
cd pyspark
python pyspark_day4_2.py
```

> **Note:** `pyspark_class.py`, `pyspark_day2.py`, and `pyspark_day2_exercise.py` read files from the bootcamp's Linux server (`file:///home/takeo/...`) that are not included in this repo. The remaining scripts have been updated to use local paths under `data/` and `project6-Covid-19_data_analysis/`.
