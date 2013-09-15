-- take 1 second to execute
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

CREATE  TABLE `moocdb`.`countries` (
  `country_code` VARCHAR(15) NOT NULL ,
  `country_population` INT(11) NULL ,
  `country_number_of_users` INT(11) NULL ,
  PRIMARY KEY (`country_code`) );