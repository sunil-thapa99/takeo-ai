from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, IntegerType, LongType
from pyspark.sql import SparkSession

'''
Scenario: You have a dataset of movie ratings submitted by users. The goal is to analyze user preferences, average ratings, and identify popular movies. The dataset contains the following columns: 

• user_id: ID of the user 

• movie_id: ID of the movie 

• rating: Rating given by the user (1-5 scale) 

• timestamp: Time of the rating 
'''

def main(df):
    # Filter
    df_filtered = df.filter(df.rating >= 4)

    # Handle Null values
    average_ratings = df.selectExpr("avg(rating)").collect()[0][0]
    df_filled = df.na.fill({"rating": average_ratings})

    # Drop Dubplicates
    df_dropped = df.dropDuplicates(["user_id", "movie_id"])

    # select specific columns
    df_selected = df.select("user_id", "rating")
    df_selected.show()


if __name__ == '__main__':
    spark = SparkSession.builder.appName("Movie Ratings Analysis").getOrCreate()
    columns = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("movie_id", IntegerType(), True),
        StructField("rating", IntegerType(), True),
        StructField("timestamp", LongType(), True),
    ])
    data = [
        (1, 101, 4, 1622388000000),
        (1, 102, 3, 1622388020000),
        (2, 101, 5, 1622388040000),
        (2, 103, 4, 1622388060000),
        (3, 101, 3, 1622388080000),
        (3, 102, 4, 1622388100000),
        (3, 103, None, 1622388120000),
        (4, 101, 2, 1622388140000)
    ]

    df = spark.createDataFrame(data, columns)

    main(df)
