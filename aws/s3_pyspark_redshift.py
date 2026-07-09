import os
import subprocess
import sys

from pyspark.sql import SparkSession
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])

load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", ACCESS_KEY)
hadoop_conf.set("fs.s3a.secret.key", SECRET_KEY)
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

df = spark.read.csv("s3a://glue-bucket-st/bootcamp/customers/customers.csv", header=True, inferSchema=True)
df.show()

df.write.format("jdbc").option("url", "jdbc:redshift://default-workgroup.746491202844.us-east-1.redshift-serverless.amazonaws.com:5439/dev")\
    .option("dbtable", "dev.test.customers")\
.option("driver","com.amazon.redshift.jdbc42.Driver").option("user", USERNAME)\
.option("password", PASSWORD).mode("overwrite").save()


# spark-submit --jars ~/redshift-jdbc42-2.1.0.9.jar --packages org.apache.hadoop:hadoop-aws:3.3.4 filename.py