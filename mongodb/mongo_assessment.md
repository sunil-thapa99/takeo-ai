1. 
db.createCollection('youtube')

db.youtube.insert({
  "kind": "youtube#searchListResponse",
  "etag": "\"m2yskBQFythfE4irbTIeOgYYfBU/PaiEDiVxOyCWelLPuuwa9LKz3Gk\"",
  "nextPageToken": "CAUQAA",
  "regionCode": "KE",
  "pageInfo": {
    "totalResults": 4249,
    "resultsPerPage": 5
  },
  "items": [
    {
      "kind": "youtube#searchResult",
      "etag": "\"m2yskBQFythfE4irbTIeOgYYfBU/QpOIr3QKlV5EUlzfFcVvDiJT0hw\"",
      "id": {
        "kind": "youtube#channel",
        "channelId": "UCJowOS1R0FnhipXVqEnYU1A"
      }
    },
    {
      "kind": "youtube#searchResult",
      "etag": "\"m2yskBQFythfE4irbTIeOgYYfBU/AWutzVOt_5p1iLVifyBdfoSTf9E\"",
      "id": {
        "kind": "youtube#video",
        "videoId": "Eqa2nAAhHN0"
      }
    },
    {
      "kind": "youtube#searchResult",
      "etag": "\"m2yskBQFythfE4irbTIeOgYYfBU/2dIR9BTfr7QphpBuY3hPU-h5u-4\"",
      "id": {
        "kind": "youtube#video",
        "videoId": "IirngItQuVs"
      }
    }
  ]
})

2. db.youtube.find(
    {"items.id.channelId": "UCJowOS1R0FnhipXVqEnYU1A"},
    {"_id": 0, "regionCode": 1}
)

3. 
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri", "mongodb+srv://admin:admin@pass.srclink.mongodb.net/sampledb.youtube").load()

df.writeColumn("item", explode("items")).filter(col("item.id.channelId") == "UCJowOS1R0FnhipXVqEnYU1A" ).select("regionCode").show()


4. 
df = spark.read.format("csv").options(header=True, inferSchema=True, delimiter=',').load(
        'file:///home/takeo/sales.csv')

(df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("uri","mongodb+srv://admin:password@srclink.mongodb.net/sampledb.sales").save())