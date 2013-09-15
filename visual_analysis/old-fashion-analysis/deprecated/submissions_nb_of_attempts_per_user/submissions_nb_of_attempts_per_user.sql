-- take 5 seconds to execute
-- Created on July 2, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT COUNT(*) AS count FROM moocdb.submissions2 GROUP BY user_id ORDER BY count DESC;