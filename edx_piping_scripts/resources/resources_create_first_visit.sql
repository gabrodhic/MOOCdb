-- Takes 1 second
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

ALTER TABLE `moocdb`.`resources` 
ADD COLUMN `resource_first_visit` INT NULL , 
ADD COLUMN `resource_first_visit_certificate` INT NULL , 
ADD COLUMN `resource_week` INT NULL ,

  ADD CONSTRAINT `resource_first_visit_fk`
  FOREIGN KEY (`resource_first_visit` )
  REFERENCES `moocdb`.`observed_events` (`observed_event_id` )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION, 
  ADD CONSTRAINT `resource_first_visit_certificate_fk`
  FOREIGN KEY (`resource_first_visit_certificate` )
  REFERENCES `moocdb`.`observed_events` (`observed_event_id` )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION
, ADD INDEX `resource_first_visit_fk_idx` (`resource_first_visit` ASC) 
, ADD INDEX `resource_first_visit_certificate_fk_idx` (`resource_first_visit_certificate` ASC) ;
