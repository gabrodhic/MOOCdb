
-- -----------------------------------------------------
-- Table problem_types
-- -----------------------------------------------------


CREATE TABLE  problem_types (
  problem_type_id INT NOT NULL,
  problem_type_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (problem_type_id))
;


-- -----------------------------------------------------
-- Table resource_types
-- -----------------------------------------------------


CREATE TABLE  resource_types (
  resource_type_id INT NOT NULL,
  resource_type_content VARCHAR(20) NOT NULL,
  resource_type_medium VARCHAR(20) NOT NULL,
  PRIMARY KEY (resource_type_id))

;


-- -----------------------------------------------------
-- Table resources
-- -----------------------------------------------------


CREATE TABLE  resources (
  resource_id INT NOT NULL IDENTITY(1,1),
  resource_name VARCHAR(555) NOT NULL,
  resource_uri VARCHAR(555) NOT NULL,
  resource_type_id INT NOT NULL,
  resource_parent_id INT NULL,
  resource_child_number INT NULL,
  resource_relevant_week INT NULL,
  resource_release_timestamp DATETIME NULL,
  PRIMARY KEY (resource_id),  
  CONSTRAINT resource_type_id_fk
    FOREIGN KEY (resource_type_id)
    REFERENCES resource_types (resource_type_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT resource_parent_id_fk
    FOREIGN KEY (resource_parent_id)
    REFERENCES resources (resource_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE NONCLUSTERED INDEX resource_uri_idx ON resources(resource_uri ASC);
CREATE NONCLUSTERED INDEX resource_type_idx ON resources(resource_type_id ASC);
CREATE NONCLUSTERED INDEX resource_parent_id_idx ON resources(resource_parent_id ASC);


-- -----------------------------------------------------
-- Table problems
-- -----------------------------------------------------


CREATE TABLE  problems (
  problem_id INT NOT NULL IDENTITY(1,1),
  problem_name VARCHAR(60) NOT NULL,
  problem_parent_id INT NULL,
  problem_child_number INT NULL,
  problem_type_id INT NOT NULL,
  problem_release_timestamp DATETIME NULL,
  problem_soft_deadline DATETIME NULL,
  problem_hard_deadline DATETIME NULL,
  problem_max_submission INT NULL,
  problem_max_duration INT NULL,
  problem_weight INT NULL,
  resource_id INT NULL,
  PRIMARY KEY (problem_id),
  
  
  
  
  CONSTRAINT problem_parent_id_fk
    FOREIGN KEY (problem_parent_id)
    REFERENCES problems (problem_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT problem_type_id_fk
    FOREIGN KEY (problem_type_id)
    REFERENCES problem_types (problem_type_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT problems_resource_id_fk
    FOREIGN KEY (resource_id)
    REFERENCES resources (resource_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)


;

CREATE NONCLUSTERED INDEX problem_name_idx ON problems(problem_name ASC);
CREATE NONCLUSTERED INDEX problem_parent_id_idx ON problems(problem_parent_id ASC);
CREATE NONCLUSTERED INDEX problem_type_id_idx ON problems(problem_type_id ASC);
CREATE NONCLUSTERED INDEX resource_id_idx ON problems(resource_id ASC);


-- -----------------------------------------------------
-- Table user_types
-- -----------------------------------------------------


CREATE TABLE  user_types (
  user_type_id INT NOT NULL,
  user_type_name VARCHAR(45) NULL,
  PRIMARY KEY (user_type_id))
;


-- -----------------------------------------------------
-- Table users
-- -----------------------------------------------------


CREATE TABLE  users (
  user_id INT NOT NULL,
  user_name VARCHAR(30) NULL,
  user_gender TINYINT NULL,
  user_birthdate DATE NULL,
  user_country VARCHAR(3) NULL,
  user_ip INT NULL,
  user_timezone_offset INT NULL,
  user_final_grade FLOAT NULL,
  user_join_timestamp DATETIME NULL,
  user_os INT NULL,
  user_agent INT NULL,
  user_language INT NULL,
  user_screen_resolution VARCHAR(45) NULL,
  user_type_id INT NULL,
  
  
  PRIMARY KEY (user_id),
  
  CONSTRAINT user_type_id_fk
    FOREIGN KEY (user_type_id)
    REFERENCES user_types (user_type_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

;

CREATE NONCLUSTERED INDEX username ON users(user_name ASC);
CREATE NONCLUSTERED INDEX id ON users(user_id ASC);
CREATE NONCLUSTERED INDEX user_type_id_fk_idx ON users(user_type_id ASC);

-- -----------------------------------------------------
-- Table submissions
-- -----------------------------------------------------


CREATE TABLE  submissions (
  submission_id INT NOT NULL IDENTITY(1,1),
  user_id INT NOT NULL,
  problem_id INT NOT NULL,
  submission_timestamp DATETIME NOT NULL,
  submission_attempt_number INT NOT NULL,
  submission_answer TEXT NOT NULL,
  submission_is_submitted BIT NOT NULL,
  submission_ip INT NULL,
  submission_os INT NULL,
  submission_agent INT NULL,
  PRIMARY KEY (submission_id),
  
  
  
  CONSTRAINT problem_id_fk
    FOREIGN KEY (problem_id)
    REFERENCES problems (problem_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT submissions_user_id_fk
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)


;

CREATE NONCLUSTERED INDEX user_id ON submissions(user_id ASC, problem_id ASC);
CREATE NONCLUSTERED INDEX user_idx ON submissions(user_id ASC);
CREATE NONCLUSTERED INDEX problem_idx ON submissions(problem_id ASC);

-- -----------------------------------------------------
-- Table observed_events
-- -----------------------------------------------------


CREATE TABLE  observed_events (
  observed_event_id INT NOT NULL IDENTITY(1,1),
  user_id INT NOT NULL,
  url_id INT NOT NULL,
  observed_event_timestamp DATETIME NOT NULL,
  observed_event_duration INT NULL,
  observed_event_ip INT NULL,
  observed_event_os INT NULL,
  observed_event_agent INT NULL,
  
  
  PRIMARY KEY (observed_event_id),
  CONSTRAINT observed_events_resource_id_fk
    FOREIGN KEY (url_id)
    REFERENCES resources (resource_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT observed_events_user_id_fk
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

;


CREATE NONCLUSTERED INDEX user_id_idx ON observed_events(user_id ASC);
CREATE NONCLUSTERED INDEX resource_id_idx ON observed_events(url_id ASC);
-- -----------------------------------------------------
-- Table collaboration_types
-- -----------------------------------------------------


CREATE TABLE  collaboration_types (
  collaboration_type_id INT NOT NULL,
  collaboration_type_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (collaboration_type_id))
;


-- -----------------------------------------------------
-- Table collaborations
-- -----------------------------------------------------


CREATE TABLE  collaborations (
  collaboration_id INT NOT NULL IDENTITY(1,1),
  user_id INT NOT NULL,
  collaboration_type_id INT NOT NULL,
  collaboration_content TEXT NOT NULL,
  collaboration_timestamp DATETIME NOT NULL,
  collaboration_parent_id INT NULL,
  collaboration_child_number INT NULL,
  collaborations_ip INT NULL,
  collaborations_os INT NULL,
  collaborations_agent INT NULL,
  resource_id INT NULL,
  PRIMARY KEY (collaboration_id),
  
  
  
  
  CONSTRAINT collaborations_user_id_fk
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT collaboration_type_id_fk
    FOREIGN KEY (collaboration_type_id)
    REFERENCES collaboration_types (collaboration_type_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT collaboration_parent_id_fk
    FOREIGN KEY (collaboration_parent_id)
    REFERENCES collaborations (collaboration_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT collaborations_resource_id_fk
    FOREIGN KEY (resource_id)
    REFERENCES resources (resource_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE NONCLUSTERED INDEX user_id_idx ON collaborations(user_id ASC);
CREATE NONCLUSTERED INDEX collaboration_type_id_idx  ON collaborations(collaboration_type_id ASC);
CREATE NONCLUSTERED INDEX collaboration_parent_idx  ON collaborations(collaboration_parent_id ASC);
CREATE NONCLUSTERED INDEX resource_id_idx  ON collaborations(resource_id ASC);


-- -----------------------------------------------------
-- Table assessments
-- -----------------------------------------------------


CREATE TABLE  assessments (
  assessment_id INT NOT NULL IDENTITY(1,1),
  submission_id INT NOT NULL,
  assessment_feedback TEXT NULL,
  assessment_grade FLOAT NULL,
  assessment_grade_with_penalty FLOAT NULL,
  assessment_grader_id INT NOT NULL,
  assessment_timestamp DATETIME NULL,
  PRIMARY KEY (assessment_id),
  
 
  CONSTRAINT submission_id_fk
    FOREIGN KEY (submission_id)
    REFERENCES submissions (submission_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT assessment_grader_id_fk
    FOREIGN KEY (assessment_grader_id)
    REFERENCES users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;


CREATE NONCLUSTERED INDEX submission_id_idx ON assessments(submission_id ASC);
CREATE NONCLUSTERED  INDEX grader_id_idx ON assessments(assessment_grader_id ASC);
-- -----------------------------------------------------
-- Table surveys
-- -----------------------------------------------------


CREATE TABLE  surveys (
  survey_id INT NOT NULL IDENTITY(1,1),
  survey_start_timestamp DATETIME NULL,
  survey_end_timestamp DATETIME NULL,
  PRIMARY KEY (survey_id))
;


-- -----------------------------------------------------
-- Table questions
-- -----------------------------------------------------


CREATE TABLE  questions (
  question_id INT NOT NULL IDENTITY(1,1),
  question_content TEXT NULL,
  question_type INT NULL,
  question_reference INT NULL,
  survey_id INT NULL,
  PRIMARY KEY (question_id),
  
  CONSTRAINT survey_fk
    FOREIGN KEY (survey_id)
    REFERENCES surveys (survey_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE NONCLUSTERED INDEX survey_fk_idx ON questions(survey_id ASC);
-- -----------------------------------------------------
-- Table answers
-- -----------------------------------------------------


CREATE TABLE  answers (
  answer_id INT NOT NULL IDENTITY(1,1),
  answer_content TEXT NULL,
  PRIMARY KEY (answer_id))
;


-- -----------------------------------------------------
-- Table feedbacks
-- -----------------------------------------------------


CREATE TABLE  feedbacks (
  feedback_id INT NOT NULL IDENTITY(1,1),
  user_id INT NOT NULL,
  answer_id INT NOT NULL,
  question_id INT NOT NULL,
  feedback_timestamp DATETIME NULL,
  PRIMARY KEY (feedback_id),
  
  
  
  CONSTRAINT feedbacks_user_id_fk
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT question_id_fk
    FOREIGN KEY (question_id)
    REFERENCES questions (question_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT answer_id_fk
    FOREIGN KEY (answer_id)
    REFERENCES answers (answer_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE NONCLUSTERED INDEX user_id_fk_idx ON feedbacks(user_id ASC);
CREATE NONCLUSTERED INDEX question_id_fk_idx ON feedbacks(question_id ASC);
CREATE NONCLUSTERED INDEX answer_id_fk_idx ON feedbacks(answer_id ASC);

-- -----------------------------------------------------
-- Table urls
-- -----------------------------------------------------


CREATE TABLE  urls (
  url_id INT NOT NULL,
  url VARCHAR(255) NULL,
  PRIMARY KEY (url_id))
;


-- -----------------------------------------------------
-- Table resources_urls
-- -----------------------------------------------------


CREATE TABLE  resources_urls (
  resources_urls_id INT NOT NULL,
  resource_id INT NOT NULL,
  url_id INT NOT NULL,
  PRIMARY KEY (resources_urls_id),
  
  
  CONSTRAINT url_id_fk
    FOREIGN KEY (url_id)
    REFERENCES urls (url_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT resources_id_fk
    FOREIGN KEY (resource_id)
    REFERENCES resources (resource_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;



CREATE NONCLUSTERED INDEX url_id_fk_idx ON resources_urls(url_id ASC);
CREATE NONCLUSTERED INDEX resources_id_fk_idx ON resources_urls(resource_id ASC);

USE moocdb ;

-- -----------------------------------------------------
-- procedure load_attempts
-- -----------------------------------------------------
/*
USE moocdb;
DROP procedure IF EXISTS load_attempts;

DELIMITER $$
USE moocdb$$


CREATE DEFINER=root@localhost PROCEDURE load_attempts()
begin

-- http://stackoverflow.com/questions/5125096/for-loop-in-mysql
declare v_max int unsigned default 500;
declare v_counter int unsigned default 0;

  start transaction;
  while v_counter < v_max do
    -- insert into foo (val) values ( floor(0 + (rand() * 65535)) );

    UPDATE active as active, forum_data.courseware_studentmodule as courseware_studentmodule
    SET active.attempt = v_counter
    WHERE active.source_cw_id = courseware_studentmodule.id
    AND courseware_studentmodule.state LIKE CONCAT('%"attempts": ', v_counter, '%'); -- http://stackoverflow.com/questions/12821528/int-to-string-in-mysql

    set v_counter=v_counter+1;
  end while;
  commit;
end$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
*/
