-- Takes seconds to execute
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
UPDATE moocdb.countries AS countries
SET countries.country_number_of_users = (
	SELECT  COUNT(*)  
	FROM  moocdb.users AS users
	WHERE users.user_country = countries.country_code
	GROUP BY users.user_country
)