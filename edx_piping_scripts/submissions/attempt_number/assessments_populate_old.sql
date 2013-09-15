-- Takes  seconds to execute
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

TRUNCATE TABLE moocdb.assessments2;

-- First we get the last attempt for each problem and see if they were valid
INSERT INTO moocdb.assessments2 (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
SELECT submissions.submission_id, 'a', 1, 1, submissions.submission_timestamp
FROM moocdb.submissions2 AS submissions
WHERE submissions.submission_attempt_number = (
	SELECT MAX(submissions2.submission_attempt_number)
	FROM moocdb.submissions2 AS submissions2, moocdb.assessments AS assessments
	WHERE submissions.user_id = submissions2.user_id
		AND submissions.problem_id = submissions2.problem_id
		AND assessments.assessment_grade = 1
		AND assessments.submission_id = submissions.submission_id
)
AND submissions.user_id = 12;
;
 

INSERT INTO moocdb.assessments2 (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
SELECT submissions.submission_id, 'b', 0, 1, submissions.submission_timestamp
FROM moocdb.submissions2 AS submissions
WHERE submissions.submission_attempt_number = (
	SELECT MAX(submissions2.submission_attempt_number)
	FROM moocdb.submissions2 AS submissions2, moocdb.assessments AS assessments
	WHERE submissions.user_id = submissions2.user_id
		AND submissions.problem_id = submissions2.problem_id
		AND assessments.assessment_grade = 0
		AND assessments.submission_id = submissions.submission_id
)
AND submissions.user_id = 12;
;


-- Then we assume all other attempts for each problem are invalid
INSERT INTO moocdb.assessments2 (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
SELECT submissions.submission_id, 'c', 0, 1, submissions.submission_timestamp
FROM moocdb.submissions2 AS submissions
WHERE submissions.submission_attempt_number < (
	SELECT MAX(submissions2.submission_attempt_number)
	FROM moocdb.submissions2 AS submissions2, moocdb.assessments AS assessments
	WHERE submissions.user_id = submissions2.user_id
		AND submissions.problem_id = submissions2.problem_id
		AND assessments.assessment_grade = 1
		AND assessments.submission_id = submissions.submission_id
)
AND submissions.user_id = 12;

INSERT INTO moocdb.assessments2 (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
SELECT submissions.submission_id, 'd', 0, 1, submissions.submission_timestamp
FROM moocdb.submissions2 AS submissions
WHERE submissions.submission_attempt_number < (
	SELECT MAX(submissions2.submission_attempt_number)
	FROM moocdb.submissions2 AS submissions2, moocdb.assessments AS assessments
	WHERE submissions.user_id = submissions2.user_id
		AND submissions.problem_id = submissions2.problem_id
		AND assessments.assessment_grade = 0
		AND assessments.submission_id = submissions.submission_id
)
AND submissions.user_id = 12;