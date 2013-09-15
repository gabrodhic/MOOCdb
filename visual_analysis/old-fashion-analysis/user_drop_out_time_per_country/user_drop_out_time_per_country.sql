-- take  seconds to execute
-- Created on June 22, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- SELECT FROM_UNIXTIME(ROUND(AVG(UNIX_TIMESTAMP(user_last_event.event_time)))), users.user_country

-- Average number of days before students drop out per country
SELECT users.user_country,
	DATEDIFF(FROM_UNIXTIME(ROUND(AVG(UNIX_TIMESTAMP(user_last_event.event_time)))) , '2012-03-05 00:00:01') AS days
        
FROM moocdb.users AS users, moocdb.user_last_event AS user_last_event
WHERE users.user_id = user_last_event.user_id
GROUP BY users.user_country
HAVING COUNT(*) > 100
ORDER BY AVG(user_last_event.event_time) ASC
;
