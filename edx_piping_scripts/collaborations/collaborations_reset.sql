-- Takes 1 second to execute
-- Created on September 16, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- WARNING: this query will delete all records from the table!

SET FOREIGN_KEY_CHECKS=0;
TRUNCATE moocdb.collaborations;
ALTER TABLE moocdb.collaborations AUTO_INCREMENT = 1;
SET FOREIGN_KEY_CHECKS=1;