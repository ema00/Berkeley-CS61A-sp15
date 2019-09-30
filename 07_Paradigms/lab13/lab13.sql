.read sp17data.sql
.read su17data.sql

CREATE TABLE obedience AS
  SELECT seven, image FROM students;

CREATE TABLE smallest_int AS
  SELECT time, smallest FROM students
    WHERE smallest > 5
    ORDER BY smallest
    LIMIT 20;

CREATE TABLE greatstudents AS
  SELECT current.date, current.color, current.pet, current.number, previous.number
  FROM sp17students AS previous, students AS current
    WHERE current.date = previous.date AND current.color = previous.color AND
      current.pet = previous.pet AND current.color = previous.color;

CREATE TABLE sevens AS
  SELECT students.seven
  FROM students, checkboxes
    WHERE students.time = checkboxes.time AND students.number = 7
      AND checkboxes.'7' = 'True';

CREATE TABLE matchmaker AS
  SELECT a.pet, a.beets, a.color, b.color
  FROM students AS a, students AS b
    WHERE a.pet = b.pet AND a.beets = b.beets AND a.time < b.time;
