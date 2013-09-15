-- take  seconds to execute
-- Created on July 13, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT count(*) AS count 
FROM edx.passive
WHERE user_id IS NOT NULL 
GROUP BY user_id 
ORDER BY count DESC;