-- Takes 500 seconds to execute
-- Created on Jun 27, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

DROP PROCEDURE IF EXISTS Alter_Table;

DELIMITER $$
CREATE PROCEDURE Alter_Table()
BEGIN

	DECLARE _count INT;

	SET _count = (  SELECT COUNT(*) 
						FROM INFORMATION_SCHEMA.COLUMNS
						WHERE   TABLE_SCHEMA = 'moocdb' AND
								TABLE_NAME = 'users' AND 
								COLUMN_NAME = 'user_last_observed_event_id');

	IF _count = 0 THEN
		ALTER TABLE `moocdb`.`users` 
			ADD COLUMN `user_last_observed_event_id` INT(11) NULL;
	END IF;

	UPDATE moocdb.users AS users
		SET users.user_last_observed_event_id = (
			SELECT 
				observed_events.observed_event_id
			FROM
				moocdb.observed_events AS observed_events
			WHERE
				users.user_id = observed_events.user_id
-- 					AND users.user_id < 1000
					AND observed_events.observed_event_timestamp = (SELECT 
						MAX(observed_events.observed_event_timestamp)
					FROM
						moocdb.observed_events AS observed_events
					WHERE
						users.user_id = observed_events.user_id)
			GROUP BY observed_events.user_id

		);


END $$
DELIMITER ;

CALL Alter_Table();
DROP PROCEDURE IF EXISTS Alter_Table;
