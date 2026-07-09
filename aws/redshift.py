# pyspark --jars ~/redshift-jdbc42-2.1.0.9.jar
from pyspark.sql import SparkSession
# URL jdbc is obtained from workgroup configuration
df = spark.read.format("jdbc").option("url", "jdbc:redshift://default-workgroup.746491202844.us-east-1.redshift-serverless.amazonaws.com:5439/dev")\
    .option("dbtable", "dev.test.listing").option("driver","com.amazon.redshift.jdbc42.Driver")\
    .option("user", "admin").option("password", "pwd").load()


# SQL
df = spark.read.format("jdbc").option("url", "jdbc:redshift://default-workgroup.746491202844.us-east-1.redshift-serverless.amazonaws.com:5439/dev")\
    .option("query", "select * from dev.test.listing LIMIT 2").option("driver","com.amazon.redshift.jdbc42.Driver")\
    .option("user", "admin").option("password", "pwd").load()

df.write.format("jdbc").option("url", "jdbc:redshift://default-workgroup.746491202844.us-east-1.redshift-serverless.amazonaws.com:5439/dev")\
    .option("dbtable", "dev.test.employee")\
.option("driver","com.amazon.redshift.jdbc42.Driver").option("user", "admin")\
.option("password", "pwd").mode("overwrite").save()

# spark-submit --jars ~/redshift-jdbc42-2.1.0.9.jar filename.py

'''
https://repo1.maven.org/maven2/

pyspark --packages org.apache.hadoop:hadoop-aws:3.3.4
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", "ACCESS_KEY")
hadoop_conf.set("fs.s3a.secret.key", "SECRET_KEY")
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

df = spark.read.csv("s3a://glue-bucket-st/bootcamp/customers/customers.csv", header=True, inferSchema=True)
df.show()


# spark-submit --jars ~/redshift-jdbc42-2.1.0.9.jar --packages org.apache.hadoop:hadoop-aws:3.3.4 filename.py
'''

