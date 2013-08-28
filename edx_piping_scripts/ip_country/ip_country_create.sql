-- take 1 second to execute
-- Created on June 11, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

CREATE  TABLE `moocdb`.`ip_country` (
  `ip_start` VARCHAR(15) NOT NULL ,
  `ip_stop` VARCHAR(15) NULL ,
  `ip_numeric_start` VARCHAR(15) NULL ,
  `ip_numeric_stop` VARCHAR(15) NULL ,
  `country_code` VARCHAR(2) NULL ,
  `country_name` VARCHAR(45) NULL ,
  PRIMARY KEY (`ip_start`) ,
  INDEX `ip_numeric_start_idx` (`ip_numeric_start` ASC) ,
  INDEX `ip_numeric_stop_idx` (`ip_numeric_stop` ASC) );