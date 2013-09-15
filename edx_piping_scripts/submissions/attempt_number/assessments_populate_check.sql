-- Takes seconds to execute
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
SELECT * 
FROM moocdb.assessments2 AS assessments, moocdb.submissions2 AS submissions
WHERE submissions.submission_id = assessments.submission_id
	AND submissions.user_id = 4;

SELECT * 
FROM moocdb.assessments AS assessments, moocdb.submissions AS submissions
WHERE submissions.submission_id = assessments.submission_id
	AND submissions.user_id = 4;

SELECT * 
FROM moocdb.submissions2 AS submissions
WHERE submissions.user_id = 4;

SELECT * 
FROM moocdb.submissions AS submissions
WHERE submissions.user_id = 4;