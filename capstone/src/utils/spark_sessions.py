from pyspark.sql import SparkSession
import os 
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

REDSHIFT_URL = 'jdbc:redshift://default-workgroup.746491202844.us-east-1.redshift-serverless.amazonaws.com:5439/dev'
REDSHIFT_DRIVER = 'com.amazon.redshift.jdbc42.Driver'

def read_from_redshift(spark, table: str):
    return spark.read.format("jdbc").option("url", REDSHIFT_URL)\
            .option("user", USERNAME) \
            .option("password", PASSWORD) \
            .option("driver", REDSHIFT_DRIVER)\
            .option("dbtable", table)

def write_to_redshift(df, table: str, mode: str="overwrite"):
    df.write.format()("jdbc").option("url", REDSHIFT_URL)\
            .option("user", USERNAME) \
            .option("password", PASSWORD) \
            .option("driver", REDSHIFT_DRIVER)\
            .option("dbtable", table)\
            .mode(mode)\
            .save()
            
def get_spark_session():
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.access.key", ACCESS_KEY)
    hadoop_conf.set("fs.s3a.secret.key", SECRET_KEY)
    hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")
    return spark

if __name__ == '__main__':
    get_spark_session()
    
    