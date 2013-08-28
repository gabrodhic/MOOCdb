SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `moocdb` DEFAULT CHARACTER SET latin1 ;
USE `moocdb` ;

-- -----------------------------------------------------
-- Table `moocdb`.`problem_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`problem_types` (
  `problem_type_id` INT NOT NULL ,
  `problem_type_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`problem_type_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`problems`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`problems` (
  `problem_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `problem_name` VARCHAR(60) NOT NULL ,
  `problem_parent_id` INT NULL ,
  `problem_type_id` INT NOT NULL ,
  `problem_release_timestamp` DATETIME NULL ,
  `problem_deadline_timestamp` DATETIME NULL ,
  PRIMARY KEY (`problem_id`) ,
  INDEX `name` (`problem_name` ASC) ,
  INDEX `parent_idx` (`problem_parent_id` ASC) ,
  INDEX `type_idx` (`problem_type_id` ASC) ,
  CONSTRAINT `parent`
    FOREIGN KEY (`problem_parent_id` )
    REFERENCES `moocdb`.`problems` (`problem_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `type`
    FOREIGN KEY (`problem_type_id` )
    REFERENCES `moocdb`.`problem_types` (`problem_type_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 256
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`users`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`users` (
  `user_id` INT(11) NOT NULL ,
  `user_name` VARCHAR(30) NULL ,
  `user_gender` TINYINT NULL ,
  `user_birthdate` DATE NULL ,
  `user_country` VARCHAR(3) NULL ,
  `user_IP` INT UNSIGNED NULL ,
  `user_timezone_offset` INT NULL ,
  INDEX `username` (`user_name` ASC) ,
  INDEX `id` (`user_id` ASC) ,
  PRIMARY KEY (`user_id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`submissions`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`submissions` (
  `submission_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `user_id` INT(11) NOT NULL ,
  `problem_id` INT(11) NOT NULL ,
  `submission_timestamp` DATETIME NOT NULL ,
  `submission_attempt_number` INT(11) NOT NULL ,
  `submission_answer` VARCHAR(45) NOT NULL ,
  `grader_id` INT NOT NULL ,
  PRIMARY KEY (`submission_id`) ,
  INDEX `user_id` (`user_id` ASC, `problem_id` ASC) ,
  INDEX `user_idx` (`user_id` ASC) ,
  INDEX `problem_idx` (`problem_id` ASC) ,
  INDEX `grader_idx` (`grader_id` ASC) ,
  CONSTRAINT `problem`
    FOREIGN KEY (`problem_id` )
    REFERENCES `moocdb`.`problems` (`problem_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user`
    FOREIGN KEY (`user_id` )
    REFERENCES `moocdb`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `grader`
    FOREIGN KEY (`grader_id` )
    REFERENCES `moocdb`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 32768
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`resource_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`resource_types` (
  `resource_type_id` INT(11) NOT NULL ,
  `resource_type_name` VARCHAR(20) NOT NULL ,
  PRIMARY KEY (`resource_type_id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`resources`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`resources` (
  `resource_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `resource_name` VARCHAR(555) NOT NULL ,
  `resource_url` VARCHAR(555) NOT NULL ,
  `resource_type_id` INT(2) NOT NULL ,
  PRIMARY KEY (`resource_id`) ,
  INDEX `location` (`resource_url` ASC) ,
  INDEX `resource_type_idx` (`resource_type_id` ASC) ,
  CONSTRAINT `resource_type`
    FOREIGN KEY (`resource_type_id` )
    REFERENCES `moocdb`.`resource_types` (`resource_type_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 915
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`observed_events`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`observed_events` (
  `observed_event_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `user_id` INT(11) NOT NULL ,
  `resource_id` INT(11) NOT NULL ,
  `observed_event_timestamp` DATETIME NOT NULL ,
  `observed_event_duration` INT(11) NULL ,
  INDEX `user_idx` (`user_id` ASC) ,
  INDEX `resource_passive_idx` (`resource_id` ASC) ,
  PRIMARY KEY (`observed_event_id`) ,
  CONSTRAINT `resource_passive`
    FOREIGN KEY (`resource_id` )
    REFERENCES `moocdb`.`resources` (`resource_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_passive`
    FOREIGN KEY (`user_id` )
    REFERENCES `moocdb`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `moocdb`.`collaboration_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`collaboration_types` (
  `collaboration_type_id` INT NOT NULL ,
  `collaboration_type_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`collaboration_type_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`collaborations`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`collaborations` (
  `collaboration_id` INT NOT NULL AUTO_INCREMENT ,
  `user_id` INT NOT NULL ,
  `collaboration_type_id` INT NOT NULL ,
  `collaboration_text` VARCHAR(45) NOT NULL ,
  `collaboration_timestamp` DATETIME NOT NULL ,
  `collaboration_parent_id` INT NULL ,
  PRIMARY KEY (`collaboration_id`) ,
  INDEX `user_id_idx` (`user_id` ASC) ,
  INDEX `action_idx` (`collaboration_type_id` ASC) ,
  INDEX `parent_idx` (`collaboration_parent_id` ASC) ,
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `moocdb`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `action`
    FOREIGN KEY (`collaboration_type_id` )
    REFERENCES `moocdb`.`collaboration_types` (`collaboration_type_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `collaboration_parent`
    FOREIGN KEY (`collaboration_parent_id` )
    REFERENCES `moocdb`.`collaborations` (`collaboration_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moocdb`.`assessments`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moocdb`.`assessments` (
  `assessment_id` INT NOT NULL AUTO_INCREMENT ,
  `submission_id` INT NOT NULL ,
  `assessment_feedback` TEXT NULL ,
  `assessment_grade` DOUBLE NULL ,
  `assessment_grader_id` INT NOT NULL ,
  PRIMARY KEY (`assessment_id`) ,
  INDEX `submission_idx` (`submission_id` ASC) ,
  INDEX `grader_idx` (`assessment_grader_id` ASC) ,
  CONSTRAINT `submission`
    FOREIGN KEY (`submission_id` )
    REFERENCES `moocdb`.`submissions` (`submission_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `assesment_grader`
    FOREIGN KEY (`assessment_grader_id` )
    REFERENCES `moocdb`.`users` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `moocdb` ;

-- -----------------------------------------------------
-- procedure load_attempts
-- -----------------------------------------------------

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
