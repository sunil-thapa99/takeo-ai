## Docker copy file from local machine to docker container
docker ps
docker cp /Users/sunilthapa/Desktop/Takeo\ Bootcamp/Hive/hive-class-project/Data/movies.csv pycharmcontainer2:/home/takeo/movies.csv
docker cp /Users/sunilthapa/Desktop/Takeo\ Bootcamp/Hive/hive-class-project/Data/ratings.csv pycharmcontainer2:/home/takeo/ratings.csv

CREATE EXTERNAL TABLE movies_ext (
    movieId INT,
    title STRING,
    genres STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INPATH '/home/takeo/movies.csv' INTO TABLE movies_ext;

CREATE EXTERNAL TABLE ratings_ext (
    userId INT,
    movieId INT,
    rating DOUBLE,
    `timestamp` STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INPATH '/home/takeo/ratings.csv' INTO TABLE ratings_ext;

CREATE TABLE movies (
    movieId INT,
    title STRING
)
PARTITIONED BY (genres STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;


INSERT OVERWRITE TABLE movies
PARTITION (genres)
SELECT 
    movieId,
    title,
    genres
FROM movies_ext
LIMIT 100;



CREATE TABLE ratings (
    movieId INT,
    rating DOUBLE,
    `timestamp` STRING
)
PARTITIONED BY (userId INT)
CLUSTERED BY (rating) INTO 5 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

INSERT OVERWRITE TABLE ratings
PARTITION (userId)
SELECT 
    movieId,
    rating,
    `timestamp`,
    userId
FROM ratings_ext
LIMIT 100;

### List all the movies and the ratings
SELECT
    m.movieId,
    m.title,
    COUNT(r.rating) AS rating_count
FROM movies m
LEFT JOIN ratings r
    ON m.movieId = r.movieId
GROUP BY m.movieId, m.title
ORDER BY rating_count DESC;

### List all the users and the number of ratings they have done for a movie
SELECT
    userId,
    COUNT(*) AS total_ratings
FROM ratings
GROUP BY userId
ORDER BY total_ratings DESC;

### List all the Movie IDs which have been rated (Movie Id with at least one user rating it)
SELECT DISTINCT movieId 
FROM ratings
ORDER BY movieId;

### List all the Users who have rated the movies (Users who have rated at least one movie)
SELECT DISTINCT userId
FROM ratings
ORDER BY userId;

### List of all the User with the max ,min ,average ratings they have given against any movie
SELECT
    userId,
    MAX(rating) AS max_rating,
    MIN(rating) AS min_rating,
    ROUND(AVG(rating), 2) AS avg_rating
FROM ratings
GROUP BY userId
ORDER BY userId;

### List all the Movies with the max ,min, average ratings given by any user
SELECT
    m.movieId,
    m.title,
    MAX(r.rating) AS max_rating,
    MIN(r.rating) AS min_rating,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM movie m
JOIN rating r
    ON m.movieId = r.movieId
GROUP BY m.movieId, m.title
ORDER BY m.movieId;

