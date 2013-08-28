-- Takes 4 seconds to execute IF THE FOLLOWING INDEX IS CREATED (will take forever otherwise)
-- Created on Jun 27, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- First create index: (takes 1 second to run)
-- ALTER TABLE `moocdb`.`collaborations` 
-- ADD INDEX `user-timestamp_idx` (`user_id` ASC, `collaboration_timestamp` ASC) ;



DROP PROCEDURE IF EXISTS Alter_Table;

DELIMITER $$
CREATE PROCEDURE Alter_Table()
BEGIN

	DECLARE _count INT;

	SET _count = (  SELECT COUNT(*) 
						FROM INFORMATION_SCHEMA.COLUMNS
						WHERE   TABLE_SCHEMA = 'moocdb' AND
								TABLE_NAME = 'users' AND 
								COLUMN_NAME = 'user_last_collaboration_id');

	IF _count = 0 THEN
		ALTER TABLE `moocdb`.`users` 
			ADD COLUMN `user_last_collaboration_id` INT(11) NULL;
	END IF;

	UPDATE moocdb.users AS users
		SET users.user_last_collaboration_id = (
			SELECT 
				collaborations.collaboration_id
			FROM
				moocdb.collaborations AS collaborations
			WHERE
				users.user_id = collaborations.user_id
-- 					AND users.user_id < 1000
					AND collaborations.collaboration_timestamp = (SELECT 
						MAX(collaborations.collaboration_timestamp)
					FROM
						moocdb.collaborations AS collaborations
					WHERE
						users.user_id = collaborations.user_id)
			GROUP BY collaborations.user_id

		);


END $$
DELIMITER ;

CALL Alter_Table();
DROP PROCEDURE IF EXISTS Alter_Table;
