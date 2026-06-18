from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType
from pyspark.sql.functions import col, lit

def selectCol(df, fields):
    '''
         from pyspark.sql.functions import col

        df.select(col("firstname"),col("lastname")).show()

        df.select(df.columns[:3]).show()
        df.select(df.columns[2:4]).show()

    '''
    return df.select(*fields)

def transformCol(df, col_name, new_col_name, transform):
    return df.withColumn(new_col_name, col(col_name).cast(transform))

def updateCol(df, col_name, new_col_name, update):
    return df.withColumn(new_col_name, col(col_name)*update)

def addCol(df, col_name, const_val):
    return df.withColumn(col_name, lit(const_val))


if __name__ == "__main__":
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

    data = [("James", "Smith", "USA", "CA"),
            ("Michael", "Rose", "USA", "NY"),
            ("Robert", "Williams", "USA", "CA"),
            ("Maria", "Jones", "USA", "FL")
            ]
    columns = ["firstname", "lastname", "country", "state"]
    df = spark.createDataFrame(data=data, schema=columns)
    selectCol(df, ["firstname", "lastname"]).show(truncate=False)


    data = [
        (("James", None, "Smith"), "OH", "M"),
        (("Anna", "Rose", ""), "NY", "F"),
        (("Julia", "", "Williams"), "OH", "F"),
        (("Maria", "Anne", "Jones"), "NY", "M"),
        (("Jen", "Mary", "Brown"), "NY", "M"),
        (("Mike", "Mary", "Williams"), "OH", "M")
    ]

    schema = StructType([
        StructField('name', StructType([
            StructField('firstname', StringType(), True),
            StructField('middlename', StringType(), True),
            StructField('lastname', StringType(), True)
        ])),
        StructField('state', StringType(), True),
        StructField('gender', StringType(), True)
    ])
    df = spark.createDataFrame(data=data, schema=schema)
    selectCol(df, ["name.firstname", "name.middlename", "name.lastname"]).show(truncate=False)

    data = [('James', '', 'Smith', '1991-04-01', 'M', 3000),
            ('Michael', 'Rose', '', '2000-05-19', 'M', 4000),
            ('Robert', '', 'Williams', '1978-09-05', 'M', 4000),
            ('Maria', 'Anne', 'Jones', '1967-12-01', 'F', 4000),
            ('Jen', 'Mary', 'Brown', '1980-02-17', 'F', -1)
            ]

    columns = ["firstname", "middlename", "lastname", "dob", "gender", "salary"]

    df = spark.createDataFrame(data=data, schema=columns)
    transformCol(df, "salary", "salary", "Double").printSchema()

    updateCol(df, "salary", "salary", 50).show(truncate=False)

    data = [
        ("Ford Torino", 140, 3449, "US"),
        ("Chevrolet Monte Carlo", 150, 3761, "US"),
        ("BMW 2002", 113, 2234, "Europe")
    ]
    columns = ["carr", "horsepower", "weight", "origin"]
    df = spark.createDataFrame(data=data, schema=columns)
    df = addCol(df, "AvgWeight", 200)
    df = updateCol(df, "horsepower", "kilowatt_power", 1000)
    df = df.withColumnRenamed("carr", "car")
    df.show(truncate=False)




