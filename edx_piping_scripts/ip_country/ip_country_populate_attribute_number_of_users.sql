-- take seconds to execute
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
UPDATE moocdb.ip_country AS ip_country
SET ip_country.number_of_users = (
	SELECT  COUNT(*)  
	FROM  moocdb.users AS users
	WHERE users.user_country = ip_country.country_code
	GROUP BY users.user_country
)