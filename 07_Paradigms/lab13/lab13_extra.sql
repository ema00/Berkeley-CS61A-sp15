.read lab13.sql

CREATE TABLE sp17favnum AS
  SELECT number, COUNT(*) AS count
  FROM sp17students
    GROUP BY number ORDER BY count DESC
    LIMIT 1;


CREATE TABLE sp17favpets AS
  SELECT pet, COUNT(*) AS count
  FROM sp17students
    GROUP BY pet ORDER BY count DESC
    LIMIT 10;


CREATE TABLE su17favpets AS
  SELECT pet, COUNT(*) AS count
  FROM students
    GROUP BY pet ORDER BY count DESC
    LIMIT 10;


CREATE TABLE su17dog AS
  SELECT pet, COUNT(*) AS count
  FROM students
    WHERE pet = "dog" GROUP BY pet;


CREATE TABLE su17alldogs AS
  SELECT pet, COUNT(*) AS count
  FROM students
    WHERE pet LIKE "%dog%";


CREATE TABLE obedienceimage AS
  SELECT seven, image, COUNT(*)
  FROM students
    WHERE seven = '7'
    GROUP BY image;

CREATE TABLE smallest_int_count AS
  SELECT smallest, COUNT(*)
  FROM  students
    GROUP BY smallest;
