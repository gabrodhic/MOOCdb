-- Takes 5 seconds to execute
-- Created on Aug 28, 2013
-- pre-requesite: 
-- 1. schema moocdb is present and is of version ca. EER_Diagram-20130611.mwb
-- 2. EER_Diagram-20130611_moocdb_mock.sql has been executed first to create moocdb_mock schema without data
-- 
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

USE moocdb_mock;
SET FOREIGN_KEY_CHECKS=0;

--
-- users table
--

TRUNCATE moocdb_mock.users;

INSERT INTO moocdb_mock.users (user_id, user_name, user_gender, user_birthdate, user_country, user_ip, user_timezone_offset, 
		user_final_grade, user_join_timestamp)
SELECT user_id, user_name, user_gender, user_birthdate, user_country, user_ip, user_timezone_offset, 
		user_final_grade, user_join_timestamp
FROM moocdb.users WHERE rand() <= .001 LIMIT 10000; -- ://stackoverflow.com/questions/249301/simple-random-samples-from-a-mysql-database

-- randomize user_id, user_name, user_ip and user_join_timestamp
-- We randomize user_id by reordering them
SET @n:=0;
UPDATE moocdb_mock.users
SET user_id = (@n := @n + 1);

-- http://forums.devarticles.com/mysql-development-50/random-string-in-mysql-89293.html (last post)
-- http://sixarm.com/about/mysql-create-random-data-text-strings.html
UPDATE moocdb_mock.users
SET user_name = UUID(); 

-- Gives just one IP as example
UPDATE moocdb_mock.users
SET user_ip = 3224821259;

-- Random user_join_timestamp
-- http://stackoverflow.com/questions/4546111/insert-update-random-date-in-mysql
UPDATE moocdb_mock.users
-- SET user_join_timestamp = (SELECT '2012-03-05 12:00:00' - INTERVAL FLOOR(RAND() * 100000) SECOND)
SET user_join_timestamp = (SELECT NOW() - INTERVAL FLOOR(RAND() * 100000) SECOND)
;


--
-- table `resources`
--

TRUNCATE TABLE moocdb_mock.resources;

INSERT INTO moocdb_mock.resources (resources.resource_id, resources.resource_name, resources.resource_url, resources.resource_type_id , resources.resource_parent_id)
SELECT resources.resource_id, resources.resource_name, resources.resource_url, resources.resource_type_id , 0
FROM moocdb.resources  
WHERE resources.resource_url LIKE 'http://6002x.mitx.mit.edu%'
LIMIT 100;


--
-- table `resource_types`
--

TRUNCATE TABLE moocdb_mock.resource_types;
INSERT INTO moocdb_mock.resource_types VALUES (0,'other'),(1,'video'),(2,'wiki'),
(3,'book'),(4,'profile'),(5,'problem'),(6,'exercise'),(7,'tutorial'),(8,'exam'),(9,'homework'),(10,'home'),(19,'testing');

--
-- table `observed_events`
--

TRUNCATE TABLE moocdb_mock.observed_events;

INSERT INTO moocdb_mock.observed_events (observed_events.observed_event_id, observed_events.user_id, observed_events.resource_id,
		observed_events.observed_event_timestamp, observed_events.observed_event_duration)
SELECT observed_events.observed_event_id, observed_events.user_id, observed_events.resource_id,
		observed_events.observed_event_timestamp, observed_events.observed_event_duration		
FROM moocdb.observed_events
LIMIT 200;

-- Randomize user_id
UPDATE moocdb_mock.observed_events
SET observed_events.user_id =  (FLOOR( 1 + RAND( ) *100 ));


-- Randomize observed_event_duration
UPDATE moocdb_mock.observed_events
SET observed_events.observed_event_duration =  (FLOOR( 1 + RAND( ) *400 ));

-- Randomize resource_id
UPDATE moocdb_mock.observed_events
SET observed_events.resource_id =  (FLOOR( 1 + RAND( ) *25 ));

-- Randomize observed_event_ip
UPDATE moocdb_mock.observed_events
SET observed_events.observed_event_ip = 3224821259;

-- Randomize observed_event_timestamp
UPDATE moocdb_mock.observed_events
-- SET observed_events.observed_event_timestamp = (SELECT '2012-03-05 12:00:00' - INTERVAL FLOOR(RAND() * 100000) SECOND)
SET observed_events.observed_event_timestamp = (SELECT NOW() - INTERVAL FLOOR(RAND() * 100000) SECOND)
;



--
-- table `problem_types`
--

TRUNCATE TABLE moocdb_mock.problem_types;
INSERT INTO `moocdb_mock`.`problem_types` (`problem_type_id`, `problem_type_name`)
VALUES (0,'Unknown'),(1,'Homework'),(2,'Lecture quiz'),(3,'Lab'),(4,'Midterm example'),(5,'Midterm exam'), (6,'Final exam'), (7,'Sandbox');


--
-- table `problems`
--

TRUNCATE TABLE moocdb_mock.problems;

INSERT INTO moocdb_mock.problems (problems.problem_id, problems.problem_name, problems.problem_type_id, problems.problem_release_timestamp, 
		problems.problem_soft_deadline, problems.problem_hard_deadline)
SELECT problems.problem_id, problems.problem_name, problems.problem_type_id, problems.problem_release_timestamp, 
		problems.problem_soft_deadline, problems.problem_hard_deadline
FROM moocdb.problems  
LIMIT 100;


--
-- table `submissions`
--

TRUNCATE TABLE moocdb_mock.submissions;

INSERT INTO moocdb_mock.submissions (submissions.submission_id, submissions.user_id, submissions.problem_id, submissions.submission_timestamp,
		submissions.submission_attempt_number, submissions.submission_answer)
SELECT submissions.submission_id, submissions.user_id, submissions.problem_id, submissions.submission_timestamp,
		submissions.submission_attempt_number, submissions.submission_answer
FROM moocdb.submissions  
LIMIT 100;

-- Randomize user_id
UPDATE moocdb_mock.submissions
SET submissions.user_id =  (FLOOR( 1 + RAND( ) *100 ));

-- Randomize submission_timestamp
UPDATE moocdb_mock.submissions
-- SET submissions.submission_timestamp = (SELECT '2012-03-05 12:00:00' - INTERVAL FLOOR(RAND() * 100000) SECOND)
SET submissions.submission_timestamp = (SELECT NOW() - INTERVAL FLOOR(RAND() * 100000) SECOND)
;

--
-- table `assessments`
--

TRUNCATE TABLE moocdb_mock.assessments;

INSERT INTO moocdb_mock.assessments (assessments.assessment_id, assessments.submission_id, assessments.assessment_feedback, assessments.assessment_grade,
		assessments.assessment_grader_id, assessments.assessment_timestamp)
SELECT assessments.assessment_id, assessments.submission_id, assessments.assessment_feedback, assessments.assessment_grade,
		assessments.assessment_grader_id, assessments.assessment_timestamp
FROM moocdb.assessments  
LIMIT 100;

-- Randomize submission_timestamp
UPDATE moocdb_mock.assessments
-- SET assessments.assessment_timestamp = (SELECT '2012-03-05 12:00:00' - INTERVAL FLOOR(RAND() * 100000) SECOND)
SET assessments.assessment_timestamp = (SELECT NOW() - INTERVAL FLOOR(RAND() * 100000) SECOND)
;


--
-- table `collaborations`
--

TRUNCATE TABLE moocdb_mock.collaborations;

INSERT INTO moocdb_mock.collaborations ( collaborations.collaboration_id, collaborations.user_id, collaborations.collaboration_type_id, 
		collaborations.collaboration_content, collaborations.collaboration_timestamp, collaborations.collaboration_parent_id)
SELECT collaborations.collaboration_id, collaborations.user_id, collaborations.collaboration_type_id, 
		collaborations.collaboration_content, collaborations.collaboration_timestamp, collaborations.collaboration_parent_id
FROM moocdb.collaborations  
LIMIT 100;

-- Randomize user_id
UPDATE moocdb_mock.collaborations
SET collaborations.user_id =  (FLOOR( 1 + RAND( ) *100 ));

-- Randomize collaboration_timestamp
UPDATE moocdb_mock.collaborations
-- SET collaborations.collaboration_timestamp = (SELECT '2012-03-05 12:00:00' - INTERVAL FLOOR(RAND() * 100000) SECOND)
SET collaborations.collaboration_timestamp = (SELECT NOW() - INTERVAL FLOOR(RAND() * 100000) SECOND)
;

UPDATE moocdb_mock.collaborations
SET collaborations.collaboration_content = 'blabla this is my post'

-- SET FOREIGN_KEY_CHECKS=1;