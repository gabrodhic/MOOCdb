-- Takes less than one second to execute
SELECT user_country, (count(*) / countries.country_population * 100) AS percentage 
FROM moocdb.users AS users,
	moocdb.countries AS countries
WHERE countries.country_code = users.user_country
	AND countries.country_population > 50000
GROUP BY user_country 
ORDER BY percentage DESC;
-- http://countrycode.org/