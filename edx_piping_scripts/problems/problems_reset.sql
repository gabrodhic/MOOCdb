-- Takes 1 second
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- WARNING: this query will delete all records from the table!
TRUNCATE moocdb.problems;
ALTER TABLE moocdb.problems AUTO_INCREMENT = 1;