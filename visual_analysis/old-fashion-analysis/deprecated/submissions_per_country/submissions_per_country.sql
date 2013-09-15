-- take  seconds to execute
-- Created on July 2, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT users.user_country, (COUNT(*) / countries.country_number_of_users) AS average
FROM moocdb.submissions2 AS submissions, moocdb.users AS users, moocdb.countries AS countries
WHERE submissions.user_id = users.user_id
	AND users.user_country = countries.country_code
	AND countries.country_number_of_users > 50
GROUP BY users.user_country
ORDER BY average DESC;
