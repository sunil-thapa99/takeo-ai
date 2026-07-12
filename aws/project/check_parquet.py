import boto3
import os
from dotenv import load_dotenv
from pathlib import Path
import pyarrow.parquet as pq
import pyarrow.fs as fs

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

ARN_PERM = os.getenv("ARN_PERM")
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# print(s3.list_objects_v2(
#     Bucket="aws-takeo-covid-project",
#     Prefix="covid/gold/dim_date/"
# ))


filesystem = fs.S3FileSystem(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    region="us-east-1")

path = "aws-takeo-covid-project/covid/gold/dim_date/part-00000-f0e1bce4-33d6-4f84-bb50-eed1422edcad-c000.snappy.parquet"

pf = pq.ParquetFile(path, filesystem=filesystem)

print(pf.schema)

table = pq.read_table(
    path,
    filesystem=filesystem
)

print(table.schema)
print(table.column("full_date").to_pylist()[:20])

dates = table.column("full_date").to_pylist()

print("rows:", len(dates))
print("nulls:", sum(x is None for x in dates))
print("min:", min(d for d in dates if d is not None))
print("max:", max(d for d in dates if d is not None))

import datetime

bad = [
    (i, x, type(x))
    for i, x in enumerate(dates)
    if x is not None and not isinstance(x, datetime.date)
]

print("bad count:", len(bad))
print(bad[:10])

column = pf.metadata.row_group(0).column(0)

print(column.statistics)


path = "aws-takeo-covid-project/covid/gold/fact_testing_state_daily/part-00000-82ddebb6-3159-4554-bd30-b121a1170348-c000.snappy.parquet"

pf = pq.ParquetFile(path, filesystem=filesystem)

print(pf.schema)