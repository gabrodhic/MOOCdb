-- take 5 seconds to execute
-- Created on July 13, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT problem_id, COUNT(*) AS count FROM moocdb.submissions2 GROUP BY problem_id ORDER BY count DESC;cd 