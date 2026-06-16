For container_id select the container, and below the name of container there is id. 

In Terminal:
`docker commit #container_id pycharmimg`

Pycharm Settings: 
1. File > settings > plugins > Docker
2. File > settings > Build, Execution, Deployment > Docker 
3. File > settings > pyspark - install
4. Connect Docker 
5. Click images that's created above > Create  Container > container name: pycharmcontainer > Modify Options > Bind mounts
6. Mount the project folder
   > Host path :/Users/sunilthapa/PyCharmMiscProject
   > Container path: /home/takeo > Apply > Run
7. Terminal > su takeo > cd
8. On the top left, make sure to change Current File from Docker

This connects your local directory to docker container. 

[NOTE: Use python3 to execute]

On docker you can run pyspark with just the command `pyspark`
On Pycharm docker container terminal, you can run python spark file using

    > python3 file.py
    > spark-submit file.py