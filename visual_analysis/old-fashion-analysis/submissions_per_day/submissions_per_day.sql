-- take 3 seconds to execute
-- Created on June 22, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT DATEDIFF(submissions.submission_timestamp, '2012-03-03 00:00:01') AS day, COUNT(*) AS count
FROM moocdb.submissions2 AS submissions
GROUP BY day 
ORDER BY day ASC;
