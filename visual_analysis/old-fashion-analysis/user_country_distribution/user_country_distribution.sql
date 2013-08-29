-- Takes less than one second to execute
SELECT user_country, count(*) as count 
FROM moocdb.users 
GROUP BY user_country 
ORDER BY count DESC;
-- http://countrycode.org/