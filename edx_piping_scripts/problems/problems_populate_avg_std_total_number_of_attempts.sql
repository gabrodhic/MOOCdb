-- Takes 1000 seconds to execute
-- Created on Jun 30, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- Takes 1 second to execute
ALTER TABLE `moocdb`.`problems` 
ADD COLUMN `problem_avg_number_of_attempts` DOUBLE NULL ,
ADD COLUMN `problem_std_number_of_attempts` DOUBLE NULL ,
ADD COLUMN `problem_total_number_of_attempts` INT(7) NULL ;


-- Takes 500 seconds to execute
UPDATE moocdb.problems AS problems
SET problems.problem_avg_number_of_attempts = (
	SELECT AVG(submissions.submission_attempt_number)
	FROM moocdb.submissions AS submissions
	WHERE submissions.problem_id = problems.problem_id
		AND submissions.submission_attempt_number = (
			SELECT MAX(submissions2.submission_attempt_number)
			FROM moocdb.submissions AS submissions2
			WHERE submissions2.problem_id = submissions.problem_id
				AND submissions2.user_id = submissions.user_id
		)
	)
;


-- Takes 480 seconds to execute
UPDATE moocdb.problems AS problems
SET problems.problem_std_number_of_attempts = (
	SELECT STD(submissions.submission_attempt_number)
	FROM moocdb.submissions AS submissions
	WHERE submissions.problem_id = problems.problem_id
		AND submissions.submission_attempt_number = (
			SELECT MAX(submissions2.submission_attempt_number)
			FROM moocdb.submissions AS submissions2
			WHERE submissions2.problem_id = submissions.problem_id
				AND submissions2.user_id = submissions.user_id
		)
	)
;


-- Takes 10 seconds to execute
UPDATE moocdb.problems AS problems
SET problems.problem_total_number_of_attempts = (
	SELECT COUNT(*)
	FROM moocdb.submissions AS submissions
	WHERE submissions.problem_id = problems.problem_id
)
;
