from pyspark.sql import SparkSession
import pyspark

from pyspark.sql.types import StructType,StructField, StringType, IntegerType

def wordCount(spark, file_path):
    rdd = spark.sparkContext.textFile(file_path)
    rdd1 = rdd.flatMap(lambda x: x.split(" "))
    print(rdd1.collect())
    rdd2 = rdd1.map(lambda x: (x, 1))
    rdd3 = rdd2.reduceByKey(lambda a, b: a + b)
    print(rdd3.collect())
    rdd4 = rdd3.map(lambda x: (x[1], x[0])).sortByKey()
    rdd5 = rdd4.filter(lambda x: 'wind' in x[1])
    print(rdd5.collect())

def convertDF(spark, columns, data):
    rdd = spark.sparkContext.parallelize(data)
    dfFromRDD = rdd.toDF(columns)
    print(dfFromRDD.printSchema)
    print(dfFromRDD.show())

def structDF(spark, data, columns):
    df = spark.createDataFrame(data=data, schema=columns)
    print(df.printSchema)
    print(df.show())



if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    wordCount(spark=spark, file_path="file:///home/takeo/test1.txt")
    columns = ["language", "users_count"]
    data = [("Java", "20000"), ("Python", "100000"), ("Scala", "3000")]
    convertDF(spark, columns, data)

    print('-'*5, ' Struct DataFrame ', '-'*5)
    structDF(spark, data, columns)
    data = [("James", "", "Smith", "36636", "M", 3000),
            ("Michael", "Rose", "", "40288", "M", 4000),
            ("Robert", "", "Williams", "42114", "M", 4000),
            ("Maria", "Anne", "Jones", "39192", "F", 4000),
            ("Jen", "Mary", "Brown", "", "F", -1)
            ]

    schema = StructType([
        StructField("firstname", StringType(), True),
        StructField("middlename", StringType(), True),
        StructField("lastname", StringType(), True),
        StructField("id", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("salary", IntegerType(), True)
        ])
    structDF(spark, data, schema)

    print('-' * 5, ' Nested Struct DataFrame ', '-' * 5)
    structureData = [
        (("James", "", "Smith"), "36636", "M", 3100),
        (("Michael", "Rose", ""), "40288", "M", 4300),
        (("Robert", "", "Williams"), "42114", "M", 1400),
        (("Maria", "Anne", "Jones"), "39192", "F", 5500),
        (("Jen", "Mary", "Brown"), "", "F", -1)
    ]
    structureSchema = StructType([
        StructField('name', StructType([
            StructField('firstname', StringType(), True),
            StructField('middlename', StringType(), True),
            StructField('lastname', StringType(), True)
        ])),
        StructField('id', StringType(), True),
        StructField('gender', StringType(), True),
        StructField('salary', IntegerType(), True)
    ])
    structDF(spark, structureData, structureSchema)


