-- Takes 2500 seconds to execute
-- Created on June 15, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
ALTER TABLE `logs2`.`srv_logs` DROP COLUMN `filenum` , DROP COLUMN `agent` , DROP COLUMN `ip` , DROP COLUMN `event_source` 
, ADD INDEX `username_event_type_idx` (`username` ASC, `event_type` ASC) ;