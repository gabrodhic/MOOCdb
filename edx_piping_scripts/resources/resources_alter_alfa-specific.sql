-- Takes 1 second
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
ALTER TABLE `moocdb`.`resources` ADD COLUMN `resource_occurrences` INT NULL  AFTER `resource_type_id` ;
