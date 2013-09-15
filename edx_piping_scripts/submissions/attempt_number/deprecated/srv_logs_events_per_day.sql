-- Takes 75 seconds to execute
-- Created on June 15, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT DATEDIFF(time, '2012-03-03 00:00:01') AS day, COUNT(*) AS count
FROM logs2.srv_logs 
GROUP BY day
ORDER BY day ASC ;

