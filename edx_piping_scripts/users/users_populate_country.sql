-- Takes 10000 seconds
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

UPDATE moocdb.users as users1
SET user_country = (
	SELECT ip_country.country_code
	FROM moocdb.ip_country AS ip_country
	WHERE users1.user_ip >= ip_country.ip_numeric_start
	AND users1.user_ip <= ip_country.ip_numeric_stop
	LIMIT 1
)
;