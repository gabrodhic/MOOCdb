-- take 1 second to execute
-- Created on June 22, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT user_country, (count(*) / countries.country_population * 100) AS percentage 
FROM moocdb.users AS users,
	moocdb.countries AS countries
WHERE countries.country_code = users.user_country
	AND countries.country_population > 50000
GROUP BY user_country 
ORDER BY percentage DESC;
-- http://countrycode.org/