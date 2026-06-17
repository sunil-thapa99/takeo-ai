from pyspark.sql import SparkSession

def readRDD(spark, file_path):
    rdd = spark.sparkContext.textFile(file_path)
    return rdd

def transform(transactions_rdd):
    transactions_tuple_rdd = transactions_rdd.map(lambda line: [x.strip("'") for x in line.split(",")])
    print(transactions_tuple_rdd.collect())
    high_quantity_rdd = transactions_tuple_rdd.filter(lambda x: int(x[6]) > 1)
    print(high_quantity_rdd.collect())
    products_flat_rdd = transactions_tuple_rdd.flatMap(lambda x: [x[3]])
    print(products_flat_rdd.collect())
    pair_rdd = transactions_tuple_rdd.map(lambda x: (x[1], (x[3], float(x[5]) * int(x[6]))))
    print(pair_rdd.collect())

    return pair_rdd

def saveToFile(output_file_path, rdd):
    rdd.saveAsTextFile(output_file_path)


if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    file_path = "file:///home/takeo/sales.csv"
    transactions_rdd = readRDD(spark, file_path)
    pair_rdd = transform(transactions_rdd)

    customer_spending_rdd = pair_rdd.map(lambda x: (x[0], x[1][1])).reduceByKey(lambda x, y: x + y)
    print(customer_spending_rdd.collect())
    customer_products_rdd = pair_rdd.map(lambda x: (x[0], x[1][0])).groupByKey().mapValues(list)
    print(customer_products_rdd.collect())

    product_category_data = [
        ('Laptop', 'Electronics'),
        ('Headphones', 'Electronics'),
        ('Book', 'Books'),
        ('Chair', 'Furniture')
    ]
    product_category_rdd = spark.sparkContext.parallelize(product_category_data)
    customer_product_category_rdd = pair_rdd.map(lambda x: (x[1][0], (x[0], x[1][1]))).join(product_category_rdd)
    print(customer_product_category_rdd.collect())

    # saveToFile("output/customer_spending_rdd", customer_spending_rdd)
    # saveToFile("output/customer_products", customer_products_rdd)
    # saveToFile("output/customer_product_category", customer_product_category_rdd)

