-- Takes 130 seconds to execute
-- Created on Jun 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- Takes 4 seconds to execute
ALTER TABLE `moocdb`.`users` 
ADD COLUMN `user_number_of_attempted_problems` INT(3) NULL ,
ADD COLUMN `user_number_of_correct_problems` INT(3) NULL
;


-- Takes 20 seconds to execute
UPDATE moocdb.users AS users
SET users.user_number_of_attempted_problems = (
	SELECT COUNT(DISTINCT(submissions.problem_id)) 
	FROM moocdb.submissions AS submissions
	WHERE users.user_id = submissions.user_id
	)
;

-- Takes 110 seconds to execute
UPDATE moocdb.users AS users
SET users.user_number_of_correct_problems = (
	SELECT COUNT(DISTINCT(submissions.problem_id)) 
	FROM moocdb.submissions AS submissions,
		moocdb.assessments AS assessments		
	WHERE users.user_id = submissions.user_id
		AND assessments.submission_id = submissions.submission_id
		AND assessments.assessment_grade = 1
	)
;