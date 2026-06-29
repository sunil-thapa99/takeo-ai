from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql.functions import col, array_contains, avg, max, count

# Q1.
def q1(spark):
    # hadoop fs -put department.txt /data/test/text
    cols = StructType([
        StructField("dept_name", StringType(), True),
        StructField("dept_id", IntegerType(), True),
        StructField("salary", LongType(), True),
    ])
    df = spark.read.option("header", "false") .schema(cols).csv("/data/test/text/department.txt")
    df_double = df.withColumn("doubleSalary", col("salary")*2)
    selected_col = df_double.select("dept_name", "salary", "doubleSalary")
    selected_col.write.mode("overwrite").parquet("/data/test/text/department_double.parquet")

# Q2.
def q2(spark):
    df = spark.read.json("file:///home/takeo/student.json")
    df.filter(
        array_contains(col("languages"), "Java") & (col("state") != "OH")
    ).select(
        col("name.firstname").alias("firstname"),
        col("gender")
    ).show()


# Q3
def q3(spark):
    df = spark.read.json("file:///home/takeo/employee.json")
    df_distinct = df.dropDuplicates()
    df_distinct.write \
        .mode("overwrite") \
        .partitionBy("department") \
        .orc("/data/test/text/employee_orc")
    mean_salary = df_distinct.groupBy("department").agg(avg("salary").alias("salary")).orderBy(col("salary").desc())
    mean_salary.show()

# Q4
def q4(spark):
    print(spark.conf.get("spark.sql.catalogImplementation"))
    emp_df = spark.read.json("file:///home/takeo/employee.json")
    dept_df = spark.read.json("file:///home/takeo/department.json")
    joined = emp_df.join(dept_df, emp_df.emp_dept_id == dept_df.dept_id, "inner")
    result = joined.groupBy("dept_name") \
        .agg(
        max("salary").alias("maxSalary"),
        count("emp_id").alias("employeesCount")
    )
    spark.sql("DROP TABLE IF EXISTS default.part_department")
    spark.sql("""
              CREATE TABLE default.part_department
              (
                  maxSalary LONG,
                  employeesCount LONG
              ) PARTITIONED BY (dept_name STRING)
        STORED AS PARQUET
              """)
    spark.conf.set("hive.exec.dynamic.partition", "true")
    spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
    result.select("maxSalary", "employeesCount", "dept_name") \
        .write \
        .mode("overwrite") \
        .insertInto("default.part_department")
    spark.sql("SELECT * FROM default.part_department").show()

# Q5
def q5(spark):
    df = spark.read.option("header", "true").option("inferSchema", "true").csv("file:///home/takeo/simple-zipcodes.csv")
    sampled_df = df.sample(fraction=0.5, seed=42)
    print(f"Sampled records (50%): {sampled_df.count()}")
    spark.sql("DROP TABLE IF EXISTS default.zipcode_partitioned")

    spark.sql("""
              CREATE TABLE IF NOT EXISTS default.zipcode_partitioned
              (
                  RecordNumber INT,
                  Country STRING,
                  Zipcode INT
              )
                  PARTITIONED BY
              (
                  State STRING,
                  City STRING
              )
                  STORED AS PARQUET
              """)
    spark.conf.set("hive.exec.dynamic.partition", "true")
    spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
    spark.conf.set("spark.sql.files.maxRecordsPerFile", "3")
    sampled_df.select("RecordNumber", "Country", "Zipcode", "State", "City") \
        .write \
        .mode("overwrite") \
        .insertInto("default.zipcode_partitioned")
    result = spark.sql("""
                       SELECT *
                       FROM default.zipcode_partitioned
                       WHERE State != 'AL' AND City != 'SPRINGVILLE'
                       """)
    result.show()



if __name__ == "__main__":
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    q1(spark)
    q2(spark)
    q3(spark)
    spark2 = SparkSession.builder.master("local[1]").appName("assessment") \
        .enableHiveSupport() \
        .getOrCreate()
    q4(spark2)
    q5(spark2)
