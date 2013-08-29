-- Takes 1 second to execute
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

