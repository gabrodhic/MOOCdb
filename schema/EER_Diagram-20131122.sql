SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `moocdb` ;
CREATE SCHEMA IF NOT EXISTS `moocdb` DEFAULT CHARACTER SET latin1 ;
USE `moocdb` ;

-- -----------------------------------------------------
-- Table `moocdb`.`problem_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`problem_types` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`problem_types` (
  `problem_type_id` INT NOT NULL,
  `problem_type_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`problem_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`resource_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`resource_types` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`resource_types` (
  `resource_type_id` INT(11) NOT NULL,
  `resource_type_content` VARCHAR(20) NOT NULL,
  `resource_type_medium` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`resource_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`resources`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`resources` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`resources` (
  `resource_id` INT(11) NOT NULL AUTO_INCREMENT,
  `resource_name` VARCHAR(555) NOT NULL,
  `resource_uri` VARCHAR(555) NOT NULL,
  `resource_type_id` INT(2) NOT NULL,
  `resource_parent_id` INT(11) NULL,
  `resource_child_number` INT NULL,
  `resource_relevant_week` INT NULL,
  `resource_release_timestamp` DATETIME NULL,
  PRIMARY KEY (`resource_id`),
  INDEX `resource_uri_idx` (`resource_uri` ASC),
  INDEX `resource_type_idx` (`resource_type_id` ASC),
  INDEX `resource_parent_id_idx` (`resource_parent_id` ASC),
  CONSTRAINT `resource_type_id_fk`
    FOREIGN KEY (`resource_type_id`)
    REFERENCES `moocdb`.`resource_types` (`resource_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `resource_parent_id_fk`
    FOREIGN KEY (`resource_parent_id`)
    REFERENCES `moocdb`.`resources` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 915
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`problems`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`problems` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`problems` (
  `problem_id` INT(11) NOT NULL AUTO_INCREMENT,
  `problem_name` VARCHAR(60) NOT NULL,
  `problem_parent_id` INT NULL,
  `problem_child_number` INT NULL,
  `problem_type_id` INT NOT NULL,
  `problem_release_timestamp` DATETIME NULL,
  `problem_soft_deadline` DATETIME NULL,
  `problem_hard_deadline` DATETIME NULL,
  `problem_max_submission` INT NULL,
  `problem_max_duration` INT NULL,
  `problem_weight` INT NULL,
  `resource_id` INT NULL,
  PRIMARY KEY (`problem_id`),
  INDEX `problem_name_idx` (`problem_name` ASC),
  INDEX `problem_parent_id_idx` (`problem_parent_id` ASC),
  INDEX `problem_type_id_idx` (`problem_type_id` ASC),
  INDEX `resource_id_idx` (`resource_id` ASC),
  CONSTRAINT `problem_parent_id_fk`
    FOREIGN KEY (`problem_parent_id`)
    REFERENCES `moocdb`.`problems` (`problem_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `problem_type_id_fk`
    FOREIGN KEY (`problem_type_id`)
    REFERENCES `moocdb`.`problem_types` (`problem_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `problems_resource_id_fk`
    FOREIGN KEY (`resource_id`)
    REFERENCES `moocdb`.`resources` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 256
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`user_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`user_types` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`user_types` (
  `user_type_id` INT NOT NULL,
  `user_type_name` VARCHAR(45) NULL,
  PRIMARY KEY (`user_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`users` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`users` (
  `user_id` INT(11) NOT NULL,
  `user_name` VARCHAR(30) NULL,
  `user_gender` TINYINT NULL,
  `user_birthdate` DATE NULL,
  `user_country` VARCHAR(3) NULL,
  `user_ip` INT UNSIGNED NULL,
  `user_timezone_offset` INT NULL,
  `user_final_grade` DOUBLE NULL,
  `user_join_timestamp` DATETIME NULL,
  `user_os` INT NULL,
  `user_agent` INT NULL,
  `user_language` INT NULL,
  `user_screen_resolution` VARCHAR(45) NULL,
  `user_type_id` INT NULL,
  INDEX `username` (`user_name` ASC),
  INDEX `id` (`user_id` ASC),
  PRIMARY KEY (`user_id`),
  INDEX `user_type_id_fk_idx` (`user_type_id` ASC),
  CONSTRAINT `user_type_id_fk`
    FOREIGN KEY (`user_type_id`)
    REFERENCES `moocdb`.`user_types` (`user_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`submissions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`submissions` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`submissions` (
  `submission_id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `problem_id` INT(11) NOT NULL,
  `submission_timestamp` DATETIME NOT NULL,
  `submission_attempt_number` INT(11) NOT NULL,
  `submission_answer` TEXT NOT NULL,
  `submission_is_submitted` BIT NOT NULL,
  `submission_ip` INT NULL,
  `submission_os` INT NULL,
  `submission_agent` INT NULL,
  PRIMARY KEY (`submission_id`),
  INDEX `user_id` (`user_id` ASC, `problem_id` ASC),
  INDEX `user_idx` (`user_id` ASC),
  INDEX `problem_idx` (`problem_id` ASC),
  CONSTRAINT `problem_id_fk`
    FOREIGN KEY (`problem_id`)
    REFERENCES `moocdb`.`problems` (`problem_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `submissions_user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `moocdb`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 32768
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`observed_events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`observed_events` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`observed_events` (
  `observed_event_id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `url_id` INT(11) NOT NULL,
  `observed_event_timestamp` DATETIME NOT NULL,
  `observed_event_duration` INT(11) NULL,
  `observed_event_ip` INT NULL,
  `observed_event_os` INT NULL,
  `observed_event_agent` INT NULL,
  INDEX `user_id_idx` (`user_id` ASC),
  INDEX `resource_id_idx` (`url_id` ASC),
  PRIMARY KEY (`observed_event_id`),
  CONSTRAINT `observed_events_resource_id_fk`
    FOREIGN KEY (`url_id`)
    REFERENCES `moocdb`.`resources` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `observed_events_user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `moocdb`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`collaboration_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`collaboration_types` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`collaboration_types` (
  `collaboration_type_id` INT NOT NULL,
  `collaboration_type_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`collaboration_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`collaborations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`collaborations` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`collaborations` (
  `collaboration_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `collaboration_type_id` INT NOT NULL,
  `collaboration_content` TEXT NOT NULL,
  `collaboration_timestamp` DATETIME NOT NULL,
  `collaboration_parent_id` INT NULL,
  `collaboration_child_number` INT NULL,
  `collaborations_ip` INT NULL,
  `collaborations_os` INT NULL,
  `collaborations_agent` INT NULL,
  `resource_id` INT NULL,
  PRIMARY KEY (`collaboration_id`),
  INDEX `user_id_idx` (`user_id` ASC),
  INDEX `collaboration_type_id_idx` (`collaboration_type_id` ASC),
  INDEX `collaboration_parent_idx` (`collaboration_parent_id` ASC),
  INDEX `resource_id_idx` (`resource_id` ASC),
  CONSTRAINT `collaborations_user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `moocdb`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `collaboration_type_id_fk`
    FOREIGN KEY (`collaboration_type_id`)
    REFERENCES `moocdb`.`collaboration_types` (`collaboration_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `collaboration_parent_id_fk`
    FOREIGN KEY (`collaboration_parent_id`)
    REFERENCES `moocdb`.`collaborations` (`collaboration_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `collaborations_resource_id_fk`
    FOREIGN KEY (`resource_id`)
    REFERENCES `moocdb`.`resources` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`assessments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`assessments` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`assessments` (
  `assessment_id` INT NOT NULL AUTO_INCREMENT,
  `submission_id` INT NOT NULL,
  `assessment_feedback` TEXT NULL,
  `assessment_grade` DOUBLE NULL,
  `assessment_grade_with_penalty` DOUBLE NULL,
  `assessment_grader_id` INT NOT NULL,
  `assessment_timestamp` DATETIME NULL,
  PRIMARY KEY (`assessment_id`),
  INDEX `submission_id_idx` (`submission_id` ASC),
  INDEX `grader_id_idx` (`assessment_grader_id` ASC),
  CONSTRAINT `submission_id_fk`
    FOREIGN KEY (`submission_id`)
    REFERENCES `moocdb`.`submissions` (`submission_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `assessment_grader_id_fk`
    FOREIGN KEY (`assessment_grader_id`)
    REFERENCES `moocdb`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`surveys`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`surveys` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`surveys` (
  `survey_id` INT NOT NULL AUTO_INCREMENT,
  `survey_start_timestamp` DATETIME NULL,
  `survey_end_timestamp` DATETIME NULL,
  PRIMARY KEY (`survey_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`questions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`questions` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`questions` (
  `question_id` INT NOT NULL AUTO_INCREMENT,
  `question_content` TEXT NULL,
  `question_type` INT NULL,
  `question_reference` INT NULL,
  `survey_id` INT NULL,
  PRIMARY KEY (`question_id`),
  INDEX `survey_fk_idx` (`survey_id` ASC),
  CONSTRAINT `survey_fk`
    FOREIGN KEY (`survey_id`)
    REFERENCES `moocdb`.`surveys` (`survey_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`answers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`answers` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`answers` (
  `answer_id` INT NOT NULL AUTO_INCREMENT,
  `answer_content` TEXT NULL,
  PRIMARY KEY (`answer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`feedbacks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`feedbacks` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`feedbacks` (
  `feedback_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `answer_id` INT NOT NULL,
  `question_id` INT NOT NULL,
  `feedback_timestamp` DATETIME NULL,
  PRIMARY KEY (`feedback_id`),
  INDEX `user_id_fk_idx` (`user_id` ASC),
  INDEX `question_id_fk_idx` (`question_id` ASC),
  INDEX `answer_id_fk_idx` (`answer_id` ASC),
  CONSTRAINT `feedbacks_user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `moocdb`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `question_id_fk`
    FOREIGN KEY (`question_id`)
    REFERENCES `moocdb`.`questions` (`question_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `answer_id_fk`
    FOREIGN KEY (`answer_id`)
    REFERENCES `moocdb`.`answers` (`answer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`urls`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`urls` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`urls` (
  `url_id` INT NOT NULL,
  `url` VARCHAR(255) NULL,
  PRIMARY KEY (`url_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`resources_urls`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `moocdb`.`resources_urls` ;

CREATE TABLE IF NOT EXISTS `moocdb`.`resources_urls` (
  `resources_urls_id` INT NOT NULL,
  `resource_id` INT NOT NULL,
  `url_id` INT NOT NULL,
  PRIMARY KEY (`resources_urls_id`),
  INDEX `url_id_fk_idx` (`url_id` ASC),
  INDEX `resources_id_fk_idx` (`resource_id` ASC),
  CONSTRAINT `url_id_fk`
    FOREIGN KEY (`url_id`)
    REFERENCES `moocdb`.`urls` (`url_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `resources_id_fk`
    FOREIGN KEY (`resource_id`)
    REFERENCES `moocdb`.`resources` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `moocdb` ;

-- -----------------------------------------------------
-- procedure load_attempts
-- -----------------------------------------------------

USE `moocdb`;
DROP procedure IF EXISTS `moocdb`.`load_attempts`;

DELIMITER $$
USE `moocdb`$$


CREATE DEFINER=`root`@`localhost` PROCEDURE `load_attempts`()
begin

-- http://stackoverflow.com/questions/5125096/for-loop-in-mysql
declare v_max int unsigned default 500;
declare v_counter int unsigned default 0;

  start transaction;
  while v_counter < v_max do
    -- insert into foo (val) values ( floor(0 + (rand() * 65535)) );

    UPDATE moocdb.active as active, forum_data.courseware_studentmodule as courseware_studentmodule
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
