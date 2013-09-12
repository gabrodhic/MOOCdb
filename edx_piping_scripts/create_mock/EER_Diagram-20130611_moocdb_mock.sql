SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `moocdb_mock` DEFAULT CHARACTER SET latin1 ;
USE `moocdb_mock` ;

-- -----------------------------------------------------
-- Table `moocdb_mock`.`problem_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`problem_types` (
  `problem_type_id` INT NOT NULL ,
  `problem_type_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`problem_type_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`problems`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`problems` (
  `problem_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `problem_name` VARCHAR(60) NOT NULL ,
  `problem_parent_id` INT NULL ,
  `problem_type_id` INT NOT NULL ,
  `problem_release_timestamp` DATETIME NULL ,
  `problem_soft_deadline` DATETIME NULL ,
  `problem_hard_deadline` DATETIME NULL ,
  `problem_max_submission` INT NULL ,
  PRIMARY KEY (`problem_id`) ,
  INDEX `name` (`problem_name` ASC) ,
  INDEX `parent_idx` (`problem_parent_id` ASC) ,
  INDEX `type_idx` (`problem_type_id` ASC) ,
  CONSTRAINT `parent`
    FOREIGN KEY (`problem_parent_id` )
    REFERENCES `moocdb_mock`.`problems` (`problem_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `type`
    FOREIGN KEY (`problem_type_id` )
    REFERENCES `moocdb_mock`.`problem_types` (`problem_type_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 256
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`users`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`users` (
  `user_id` INT(11) NOT NULL ,
  `user_name` VARCHAR(30) NULL ,
  `user_gender` TINYINT NULL ,
  `user_birthdate` DATE NULL ,
  `user_country` VARCHAR(3) NULL ,
  `user_ip` INT UNSIGNED NULL ,
  `user_timezone_offset` INT NULL ,
  `user_final_grade` DOUBLE NULL ,
  `user_join_timestamp` DATETIME NULL ,
  `user_os` INT NULL ,
  `user_agent` INT NULL ,
  `user_language` INT NULL ,
  `user_screen_resolution` VARCHAR(45) NULL ,
  INDEX `username` (`user_name` ASC) ,
  INDEX `id` (`user_id` ASC) ,
  PRIMARY KEY (`user_id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`submissions`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`submissions` (
  `submission_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `user_id` INT(11) NOT NULL ,
  `problem_id` INT(11) NOT NULL ,
  `submission_timestamp` DATETIME NOT NULL ,
  `submission_attempt_number` INT(11) NOT NULL ,
  `submission_answer` TEXT NOT NULL ,
  `submission_is_submitted` BIT NOT NULL ,
  `submission_ip` INT NULL ,
  `submission_os` INT NULL ,
  `submission_agent` INT NULL ,
  PRIMARY KEY (`submission_id`) ,
  INDEX `user_id` (`user_id` ASC, `problem_id` ASC) ,
  INDEX `user_idx` (`user_id` ASC) ,
  INDEX `problem_idx` (`problem_id` ASC) ,
  CONSTRAINT `problem`
    FOREIGN KEY (`problem_id` )
    REFERENCES `moocdb_mock`.`problems` (`problem_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user`
    FOREIGN KEY (`user_id` )
    REFERENCES `moocdb_mock`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 32768
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`resource_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`resource_types` (
  `resource_type_id` INT(11) NOT NULL ,
  `resource_type_name` VARCHAR(20) NOT NULL ,
  PRIMARY KEY (`resource_type_id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`resources`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`resources` (
  `resource_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `resource_name` VARCHAR(555) NOT NULL ,
  `resource_url` VARCHAR(555) NOT NULL ,
  `resource_type_id` INT(2) NOT NULL ,
  `resource_parent_id` INT(11) NULL ,
  PRIMARY KEY (`resource_id`) ,
  INDEX `location` (`resource_url` ASC) ,
  INDEX `resource_type_idx` (`resource_type_id` ASC) ,
  INDEX `resource_parent_id_idx` (`resource_parent_id` ASC) ,
  CONSTRAINT `resource_type`
    FOREIGN KEY (`resource_type_id` )
    REFERENCES `moocdb_mock`.`resource_types` (`resource_type_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `resource_parent_id`
    FOREIGN KEY (`resource_parent_id` )
    REFERENCES `moocdb_mock`.`resources` (`resource_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 915
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`observed_events`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`observed_events` (
  `observed_event_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `user_id` INT(11) NOT NULL ,
  `resource_id` INT(11) NOT NULL ,
  `observed_event_timestamp` DATETIME NOT NULL ,
  `observed_event_duration` INT(11) NULL ,
  `observed_event_ip` INT NULL ,
  `observed_event_os` INT NULL ,
  `observed_event_agent` INT NULL ,
  INDEX `user_idx` (`user_id` ASC) ,
  INDEX `resource_passive_idx` (`resource_id` ASC) ,
  PRIMARY KEY (`observed_event_id`) ,
  CONSTRAINT `resource_passive`
    FOREIGN KEY (`resource_id` )
    REFERENCES `moocdb_mock`.`resources` (`resource_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_passive`
    FOREIGN KEY (`user_id` )
    REFERENCES `moocdb_mock`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`collaboration_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`collaboration_types` (
  `collaboration_type_id` INT NOT NULL ,
  `collaboration_type_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`collaboration_type_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`collaborations`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`collaborations` (
  `collaboration_id` INT NOT NULL AUTO_INCREMENT ,
  `user_id` INT NOT NULL ,
  `collaboration_type_id` INT NOT NULL ,
  `collaboration_content` TEXT NOT NULL ,
  `collaboration_timestamp` DATETIME NOT NULL ,
  `collaboration_parent_id` INT NULL ,
  `collaborations_ip` INT NULL ,
  `collaborations_os` INT NULL ,
  `collaborations_agent` INT NULL ,
  PRIMARY KEY (`collaboration_id`) ,
  INDEX `user_id_idx` (`user_id` ASC) ,
  INDEX `action_idx` (`collaboration_type_id` ASC) ,
  INDEX `parent_idx` (`collaboration_parent_id` ASC) ,
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `moocdb_mock`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `action`
    FOREIGN KEY (`collaboration_type_id` )
    REFERENCES `moocdb_mock`.`collaboration_types` (`collaboration_type_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `collaboration_parent`
    FOREIGN KEY (`collaboration_parent_id` )
    REFERENCES `moocdb_mock`.`collaborations` (`collaboration_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`assessments`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`assessments` (
  `assessment_id` INT NOT NULL AUTO_INCREMENT ,
  `submission_id` INT NOT NULL ,
  `assessment_feedback` TEXT NULL ,
  `assessment_grade` DOUBLE NULL ,
  `assessment_grader_id` INT NOT NULL ,
  `assessment_timestamp` DATETIME NULL ,
  PRIMARY KEY (`assessment_id`) ,
  INDEX `submission_idx` (`submission_id` ASC) ,
  INDEX `grader_idx` (`assessment_grader_id` ASC) ,
  CONSTRAINT `submission`
    FOREIGN KEY (`submission_id` )
    REFERENCES `moocdb_mock`.`submissions` (`submission_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `assesment_grader`
    FOREIGN KEY (`assessment_grader_id` )
    REFERENCES `moocdb_mock`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`surveys`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`surveys` (
  `survey_id` INT NOT NULL AUTO_INCREMENT ,
  `survey_start_timestamp` DATETIME NULL ,
  `survey_end_timestamp` DATETIME NULL ,
  PRIMARY KEY (`survey_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`questions`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`questions` (
  `question_id` INT NOT NULL AUTO_INCREMENT ,
  `question_content` TEXT NULL ,
  `question_type` INT NULL ,
  `question_reference` INT NULL ,
  `survey_id` INT NULL ,
  PRIMARY KEY (`question_id`) ,
  INDEX `survey_fk_idx` (`survey_id` ASC) ,
  CONSTRAINT `survey_fk`
    FOREIGN KEY (`survey_id` )
    REFERENCES `moocdb_mock`.`surveys` (`survey_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`answers`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`answers` (
  `answer_id` INT NOT NULL AUTO_INCREMENT ,
  `answer_content` TEXT NULL ,
  PRIMARY KEY (`answer_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb_mock`.`feedbacks`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb_mock`.`feedbacks` (
  `feedback_id` INT NOT NULL AUTO_INCREMENT ,
  `user_id` INT NOT NULL ,
  `answer_id` INT NOT NULL ,
  `question_id` INT NOT NULL ,
  `feedback_timestamp` DATETIME NULL ,
  PRIMARY KEY (`feedback_id`) ,
  INDEX `user_fk_idx` (`user_id` ASC) ,
  INDEX `question_fk_idx` (`question_id` ASC) ,
  INDEX `answer_fk_idx` (`answer_id` ASC) ,
  CONSTRAINT `user_fk`
    FOREIGN KEY (`user_id` )
    REFERENCES `moocdb_mock`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `question_fk`
    FOREIGN KEY (`question_id` )
    REFERENCES `moocdb_mock`.`questions` (`question_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `answer_fk`
    FOREIGN KEY (`answer_id` )
    REFERENCES `moocdb_mock`.`answers` (`answer_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
