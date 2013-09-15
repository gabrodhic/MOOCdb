-- take 1 second to execute
-- Created on June 22, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT user_country, count(*) as count 
FROM moocdb.users 
GROUP BY user_country 
ORDER BY count DESC;
-- http://countrycode.org/