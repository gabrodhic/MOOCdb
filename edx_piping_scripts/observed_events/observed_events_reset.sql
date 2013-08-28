-- Takes 5 seconds for one iteration
-- Created on June 10, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- WARNING: this query will delete all records from the table!

TRUNCATE moocdb.observed_events;
ALTER TABLE moocdb.observed_events AUTO_INCREMENT = 1;