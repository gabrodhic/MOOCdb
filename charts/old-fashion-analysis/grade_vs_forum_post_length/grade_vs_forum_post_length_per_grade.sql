-- Takes 1 second to execute
SELECT users.user_final_grade, 
	SUM(LENGTH(collaborations.collaboration_content)) / letter_grade.number_of_users, 
	COUNT(*) / letter_grade.number_of_users, 
	SUM(LENGTH(collaborations.collaboration_content)) / COUNT(*)
FROM moocdb.collaborations AS collaborations,
	moocdb.users AS users,
	moocdb.letter_grade AS letter_grade
WHERE users.user_id = collaborations.user_id
	AND letter_grade.grade = users.user_final_grade
GROUP BY users.user_final_grade
ORDER BY users.user_final_grade ASC, LENGTH(collaborations.collaboration_content) DESC 
;

