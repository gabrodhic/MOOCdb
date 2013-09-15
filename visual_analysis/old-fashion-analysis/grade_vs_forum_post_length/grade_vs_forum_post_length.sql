-- take 1 second to execute
-- Created on July 13, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT users.user_final_grade, 
	SUM(LENGTH(collaborations.collaboration_content)), 
	COUNT(*), 
	SUM(LENGTH(collaborations.collaboration_content)) / COUNT(*)
FROM moocdb.collaborations AS collaborations,
	moocdb.users AS users
WHERE users.user_id = collaborations.user_id
GROUP BY users.user_id
ORDER BY users.user_final_grade ASC, LENGTH(collaborations.collaboration_content) DESC 
;

