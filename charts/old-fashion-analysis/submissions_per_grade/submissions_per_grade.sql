-- Takes 5 seconds to run
SELECT letter_grade.letter, COUNT(*) / letter_grade.number_of_users
FROM moocdb.submissions2 AS submissions, moocdb.users AS users, moocdb.letter_grade AS letter_grade
WHERE submissions.user_id = users.user_id
	AND users.user_final_grade = letter_grade.grade
GROUP BY letter_grade.letter
ORDER BY letter_grade.letter ASC;
