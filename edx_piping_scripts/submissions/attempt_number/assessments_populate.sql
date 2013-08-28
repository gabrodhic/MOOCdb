-- Takes 2000 seconds to run

-- Sometimes the maximum number of attempts is different between the table submissions (which comes from courseware table)
-- and the table submissions2 (which comes from courseware table)

TRUNCATE TABLE moocdb.assessments2;

-- First we get the last attempt for each problem and see if they were valid
-- Case 1: the last attempt is valid
INSERT INTO moocdb.assessments2 (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
SELECT submissions.submission_id, 'a', 1, 1, submissions.submission_timestamp
FROM moocdb.submissions2 AS submissions
WHERE submissions.submission_attempt_number = (
	SELECT MAX(submissions_bis.submission_attempt_number)
	FROM moocdb.submissions2 AS submissions_bis
	WHERE submissions.user_id = submissions_bis.user_id
		AND submissions.problem_id = submissions_bis.problem_id
	
)
AND 1 = (
	SELECT assessments.assessment_grade
	FROM moocdb.submissions AS submissions_old, moocdb.assessments AS assessments
	WHERE submissions.user_id = submissions_old.user_id
		AND submissions.problem_id = submissions_old.problem_id
		-- AND assessments.assessment_grade = 1
		AND assessments.submission_id = submissions_old.submission_id
)
 AND submissions.user_id < 200000;
;

-- Case 2: the last attempt is invalid
INSERT INTO moocdb.assessments2 (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
SELECT submissions.submission_id, 'b', 0, 1, submissions.submission_timestamp
FROM moocdb.submissions2 AS submissions
WHERE submissions.submission_attempt_number = (
	SELECT MAX(submissions_bis.submission_attempt_number)
	FROM moocdb.submissions2 AS submissions_bis
	WHERE submissions.user_id = submissions_bis.user_id
		AND submissions.problem_id = submissions_bis.problem_id
	
)
AND 0 = (
	SELECT assessments.assessment_grade
	FROM moocdb.submissions AS submissions_old, moocdb.assessments AS assessments
	WHERE submissions.user_id = submissions_old.user_id
		AND submissions.problem_id = submissions_old.problem_id
		-- AND assessments.assessment_grade = 1
		AND assessments.submission_id = submissions_old.submission_id
)
AND submissions.user_id < 200000;
;
 


-- Then we assume all other attempts for each problem are invalid
-- Case 3: 
INSERT INTO moocdb.assessments2 (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
SELECT submissions.submission_id, 'c', 0, 1, submissions.submission_timestamp
FROM moocdb.submissions2 AS submissions
WHERE submissions.submission_attempt_number < (
	SELECT MAX(submissions_bis.submission_attempt_number)
	FROM moocdb.submissions2 AS submissions_bis
	WHERE submissions.user_id = submissions_bis.user_id
		AND submissions.problem_id = submissions_bis.problem_id
)
AND submissions.user_id < 200000;
;


-- In theory, the following 2 queries should return the same number.
-- However submissions2 contains slightly (around 1%) more rows than assessments2.
SELECT  COUNT(*) 
FROM moocdb.submissions2 AS submissions
WHERE submissions.user_id < 200000;

SELECT  COUNT(*) 
FROM moocdb.assessments2 AS assessments;

-- The reasons for this difference is that br_logs seems to be more complete than forum_data.courseware, e.g.:
-- returns 0 row
SELECT * FROM forum_data.courseware_studentmodule
WHERE student_id = 4
AND module_type = 'problem'
AND state LIKE '%filenamex0_3_1%';

-- returns 1 row
SELECT * FROM logs.br_logs4
WHERE username = 'jmc'
AND event LIKE '%filenamex0_3_1%';

-- which means we cannot retrieve easily the grade for every submission since only
--  courseware_studentmodule contains it. This issue affects around 1% of the 
-- submission so I'll just ignore it now. This could be solve by writing a 
-- script that retrieves the correct solution for each problem and compare to the 


