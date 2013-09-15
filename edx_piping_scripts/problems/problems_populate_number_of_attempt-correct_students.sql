-- Takes 150 seconds to execute
-- Created on Jun 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- Takes 1 seconds to execute
ALTER TABLE `moocdb`.`problems` 
ADD COLUMN `problem_number_of_attempt_students` INT(6) NULL , 
ADD COLUMN `problem_number_of_correct_students` INT(6) NULL ;

-- Takes 42 seconds to execute
UPDATE `moocdb`.`problems` AS problems 
SET 
    problems.problem_number_of_attempt_students = (SELECT 
            COUNT(DISTINCT (submissions.user_id))
        FROM
            moocdb.submissions AS submissions
        WHERE
            submissions.problem_id = problems.problem_id)
;

-- Takes 100 seconds to execute
UPDATE `moocdb`.`problems` AS problems 
SET 
    problems.problem_number_of_correct_students = (SELECT 
            COUNT(DISTINCT (submissions.user_id))
        FROM
            moocdb.submissions AS submissions
                INNER JOIN
            moocdb.assessments AS assessments ON assessments.submission_id = submissions.submission_id
        WHERE
            submissions.problem_id = problems.problem_id
                AND assessments.assessment_grade = 1)
;

