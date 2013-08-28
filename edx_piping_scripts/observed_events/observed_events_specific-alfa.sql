-- Takes  seconds for one iteration
-- Created on June 18, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
ALTER TABLE `moocdb`.`observed_events` ADD COLUMN `source_br_id` INT NOT NULL  AFTER `observed_event_duration` ;
