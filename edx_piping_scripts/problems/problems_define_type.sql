
-- HW = homework
UPDATE moocdb.problems 
SET problem_type_id=1
WHERE problem_name LIKE "%filenameHW%";


-- Lecture quiz
UPDATE moocdb.problems 
SET problem_type_id=2
WHERE problem_name LIKE "%filenameL%";

-- Labs
UPDATE moocdb.problems 
SET problem_type_id=3
WHERE problem_name LIKE "%filenameLab%";

