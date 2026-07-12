### Inside the container, copy from HDFS to a local directory in the container:
hadoop fs -get /home/takeo/testing_standardized /tmp/testing_standardized

### On your Mac terminal (not inside the container), find your container:
docker ps

### Copy the directory from the container to your Mac:
docker cp <container_name>:/tmp/testing_standardized /home/takeo/pycharmproject/aws/project