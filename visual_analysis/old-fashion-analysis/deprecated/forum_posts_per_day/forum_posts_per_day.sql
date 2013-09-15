-- take 5 seconds to execute
-- Created on July 2, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT DATEDIFF(collaborations.collaboration_timestamp, '2012-03-03 00:00:01') AS day, COUNT(*) AS count
FROM moocdb.collaborations AS collaborations
WHERE collaborations.collaboration_parent_id = 1
GROUP BY day
ORDER BY day ASC ;

