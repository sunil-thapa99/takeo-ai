- Whenever you readStream, it should follow by writeStream
```
df = spark.readStream.format("delta").table("emp")

import uuid
def foreach_batch_function(df, epoch_id):
    df.write.json("/Volumes/az_takeo_databricks/default/bootcamp/output2/"+str(uuid.uuid4()))
    # df.collect()
df.writeStream.foreachBatch(foreach_batch_function).option('checkpointLocation', '/Volumes/az_takeo_databricks/default/bootcamp/checkpoints/').start()
```

%fs to access linux command on shell
```
%fs
ls /Volumes/az_takeo_databricks/default/bootcamp/output2/
```

# df = spark.readStream.format("delta").table("emp").option("startingVersion", "2") -> check (%sql describe history table_name)
this makes sure while resuming it resumes from the given version point



