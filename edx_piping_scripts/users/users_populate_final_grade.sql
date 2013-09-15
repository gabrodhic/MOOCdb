-- Takes 2 seconds
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

UPDATE moocdb.users as users
SET users.user_final_grade = (
	SELECT letter_grade.grade 
	FROM forum_data.certificates_generatedcertificate AS certificates_generatedcertificate,
		 moocdb.letter_grade AS letter_grade
	WHERE letter_grade.letter = certificates_generatedcertificate.grade
		AND users.user_id = certificates_generatedcertificate.user_id

)