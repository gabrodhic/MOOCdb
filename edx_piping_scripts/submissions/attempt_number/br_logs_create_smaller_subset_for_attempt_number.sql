-- Takes 750 seconds to execute

USE logs;

DROP TABLE IF EXISTS br_logs4;
CREATE TABLE br_logs4 AS SELECT * FROM br_logs WHERE username='sdfndsofssfsnfsosnoisdnf' AND 1=0; -- Impossible conditions to have empty table

-- CREATE TABLE doesn't keep the constraint such as AUTO_INCREMENT and primary key, so we need to re-create them
ALTER TABLE `logs`.`br_logs4` CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT  
, ADD PRIMARY KEY (`id`) ;

ALTER TABLE `logs`.`br_logs4` ADD COLUMN `problem_id` INT NULL  AFTER `event` ;

ALTER TABLE `logs`.`br_logs4` DROP COLUMN `filenum` , DROP COLUMN `agent` , DROP COLUMN `ip` , DROP COLUMN `event_source` ,
DROP COLUMN `session` , DROP COLUMN `page` , ADD INDEX `username_event_type_idx` (`username` ASC, `event_type` ASC) ;

INSERT INTO br_logs4 (username, event_type, time, event)
SELECT username, event_type, time, event FROM br_logs WHERE event_type = 10;



-- Useful queries to choose the condition on username:
-- SELECT count(*) FROM moocdb.users WHERE user_name LIKE 'ac%' AND user_ip IS NOT NULL;
-- SELECT * FROM moocdb.users WHERE user_name LIKE 'ac%' AND user_ip IS NOT NULL;