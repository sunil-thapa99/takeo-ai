CREATE SCHEMA test;

CREATE TABLE test.emp(id INT, name VARCHAR (50));

INSERT INTO test.emp (id, name)
VALUES (1, 'SUNIL');

SELECT * FROM test.emp;

CREATE TABLE test.emp1([emp id] INT, name VARCHAR (50));

SELECT * FROM test.emp1; 

CREATE TABLE test.emp2(ID INT, Name VARCHAR (50));

INSERT INTO test.emp1
VALUES (1, 'abc');

SELECT * FROM test.emp1
WHERE [emp id]=1;

=