-- Takes 1 second to execute
SELECT letter_grade.letter,  COUNT(*) 
FROM moocdb.users AS users, moocdb.letter_grade AS letter_grade
WHERE users.user_final_grade = letter_grade.grade
GROUP BY letter_grade.grade
ORDER BY letter_grade.grade DESC 
;