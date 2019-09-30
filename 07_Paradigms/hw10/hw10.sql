-------------------------------------------------------------
                                                   -- DOGS --
-------------------------------------------------------------

create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31;

create table sizes as
  select "toy" as size, 24 as min, 28 as max union
  select "mini",        28,        35        union
  select "medium",      35,        45        union
  select "standard",    45,        60;

-------------------------------------------------------------
    -- PLEASE DO NOT CHANGE ANY DOG TABLES ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT dogs.name, sizes.size
  FROM dogs, sizes
    WHERE sizes.min < dogs.height AND dogs.height <= sizes.max;

-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_height AS
  SELECT name
  FROM dogs, parents
    WHERE name = parents.child
    ORDER BY dogs.height;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
WITH siblings_same_size AS (
  SELECT dogsA.name AS sA, dogsB.name AS sB, dogsA.size AS size, parentsA.parent, parentsB.parent
  FROM size_of_dogs AS dogsA, size_of_dogs AS dogsB, parents AS parentsA, parents AS parentsB
  WHERE dogsA.size = dogsB.size AND dogsA.name = parentsA.child AND
    dogsB.name = parentsB.child AND dogsA.name < dogsB.name AND
    parentsA.parent = parentsB.parent
)
  SELECT sA || " and " || sB || " are " || size || " siblings"
  FROM siblings_same_size
    WHERE sA < sB;

-- Heights and names of dogs that are above average in height among
-- dogs whose height has the same first digit.
CREATE TABLE above_average AS
WITH aux AS (
  SELECT name, height, ROUND(height / 10) AS first_digit, AVG(height) AS avg, count(*) AS count
  FROM dogs
    GROUP BY first_digit HAVING count > 1
)
  SELECT dogs.height, dogs.name
  FROM dogs, aux
  WHERE ROUND(dogs.height / 10) = aux.first_digit AND dogs.height > aux.avg;
-------------------------------------------------------------
                                     -- EUCLID CAFE TYCOON --
-------------------------------------------------------------

-- Locations of each cafe
create table cafes as
  select "nefeli" as name, 2 as location union
  select "brewed"        , 8             union
  select "hummingbird"   , 6;

-- Menu items at each cafe
create table menus as
  select "nefeli" as cafe, "espresso" as item union
  select "nefeli"        , "bagels"           union
  select "brewed"        , "coffee"           union
  select "brewed"        , "bagels"           union
  select "brewed"        , "muffins"          union
  select "hummingbird"   , "muffins"          union
  select "hummingbird"   , "eggs";

-- All locations on the block
create table locations as
  select 1 as n union
  select 2      union
  select 3      union
  select 4      union
  select 5      union
  select 6      union
  select 7      union
  select 8      union
  select 9      union
  select 10;

-------------------------------------------------------------
   -- PLEASE DO NOT CHANGE ANY CAFE TABLES ABOVE THIS LINE --
-------------------------------------------------------------

-- Locations without a cafe
create table open_locations as
  SELECT locations.n AS n
  FROM locations, cafes
    GROUP BY locations.n HAVING MIN(ABS(locations.n - cafes.location)) > 0;

-- Items that could be placed on a menu at an open location
create table allowed as
  with item_locations(item, location) as (
    select item, location from cafes, menus where name = cafe
  )
  SELECT locations.n AS n, item_locations.item AS item
  FROM locations, item_locations
  GROUP BY locations.n, item_locations.item HAVING MIN(ABS(locations.n - item_locations.location)) > 2;
