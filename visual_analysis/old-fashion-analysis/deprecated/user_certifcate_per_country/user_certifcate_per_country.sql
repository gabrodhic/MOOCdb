-- take  seconds to execute
-- Created on July 2, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT users.user_country, COUNT(*) AS count
FROM moocdb.users AS users
WHERE users.user_final_grade >= 0.5
GROUP BY users.user_country
ORDER BY count DESC;