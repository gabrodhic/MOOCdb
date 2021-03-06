-- take  seconds to execute
-- Created on July 2, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

USE moocdb;

-- we first create a temporary table that contains the students of certificates per country
DROP VIEW IF EXISTS temp_students_per_country;
CREATE VIEW temp_students_per_country AS
SELECT users.user_country AS country, COUNT(*) AS count
		FROM moocdb.users AS users
		GROUP BY users.user_country;

-- 
SELECT users.user_country, COUNT(*) / temp_students_per_country.count AS count -- , temp_students_per_country.count
FROM moocdb.users AS users, temp_students_per_country
WHERE users.user_final_grade >= 0.5
AND temp_students_per_country.country = users.user_country
AND temp_students_per_country.count >= 100
GROUP BY users.user_country
ORDER BY count DESC 
;


DROP VIEW temp_students_per_country;