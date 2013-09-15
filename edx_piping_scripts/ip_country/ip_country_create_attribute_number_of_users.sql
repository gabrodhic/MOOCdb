-- take 1 second to execute
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
ALTER TABLE `moocdb`.`ip_country` ADD COLUMN `number_of_users` INT NULL  AFTER `country_name` ;