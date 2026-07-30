### Day 1:

cd startApps > sh restartKafka
Then open external terminal > cd installAll > cd kafka_install > sh kafkaproducer.sh
Similarly open another external terminal > cd installAll > cd kafka_install > sh kafkaconsumer.sh
write somthing on producer, if it shows on consumer, the producer / consumer is working

### Day 2:

sh restartKafka.sh
open external terminal
Follow kafka Topic Commands -1-DE-4 docx

How to send whole file from producer
create a text in external terminal.
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic firsttopic < test.txt

<!-- Connecting with pyspark -->

kafka always sends data in key-value pair

```
pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0
kafka-topics.sh --bootstrap-server localhost:9092 --topic sparktopic --create --partitions 3 --replication-factor 1

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "sparktopic") \
  .load()
# Split the lines into words
from pyspark.sql.functions import *
words = df.select(explode(split(df.value, " ")).alias("word"))

 # Generate running word count
wordCounts = words.groupBy("word").count()

 # Start running the query that prints the running counts to the console
    query = wordCounts \
          .writeStream \
          .outputMode("complete") \
          .format("console") \
          .start()
# If issue on writeStream start, restartHadoop, probably because of setting issue on docker while creating this

query.awaitTermination()

```

After starting the stream, use command for starting and sending message from producer
kafka-console-producer.sh --bootstrap-server localhost:9092 --tc sparktopic


write to kafka from spark
```
columns = ["language","users_count"]
data = [("Java", "20000"), ("Python", "100000"), ("Scala", "3000")]
rdd = spark.sparkContext.parallelize(data)
columns = ["language","users_count"]
df = rdd.toDF(columns)


from pyspark.sql.functions import concat_ws,col,lit
'''
Here the lit is literal, so each element in list are k1: "Java, 20000", .....
This is important because kafka accepts key-value pair format.
'''
df2=df.select(lit("k1").alias("key"),concat_ws(',',df.language,df.users_count).alias("value"))
df2.show(truncate=False)


# Here we are using write instead of writeStream because we are batch processing
# kafka-console-consumer.sh --topic testing1 --from-beginning --bootstrap-server localhost:9092
df2.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
  .write \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "testing1") \
  .save()

```