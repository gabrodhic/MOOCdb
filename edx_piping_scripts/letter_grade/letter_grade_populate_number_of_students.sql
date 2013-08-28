-- Takes 1 second to execute
-- Created on June 17, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- Letters can be A, B, C and D.
-- D is a special case, it correspond when the user didn't get any final grade,
-- i.e. the final grade is NULL.
UPDATE moocdb.letter_grade AS letter_grade
SET number_of_students = (
	SELECT COUNT(*) as count
	FROM moocdb.users AS users
	WHERE letter_grade.grade = users.user_final_grade
		OR (UPPER(letter_grade.letter) = 'D'
			AND users.user_final_grade IS NULL
		   )
	GROUP BY letter_grade.grade
)
;

