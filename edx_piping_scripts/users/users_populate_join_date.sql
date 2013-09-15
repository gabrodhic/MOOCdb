-- Takes 12 seconds to execute
-- Created on Jun 25, 2013
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
								COLUMN_NAME = 'user_join_timestamp');

	IF _count = 0 THEN
		ALTER TABLE `moocdb`.`users` 
			ADD COLUMN `user_join_timestamp` DATETIME NULL  AFTER `user_final_grade` ;
	END IF;

	UPDATE moocdb.users AS users
		SET users.user_join_timestamp = (
			SELECT auth_user.date_joined 
			FROM forum_data.auth_user AS auth_user
			WHERE users.user_id = auth_user.id
		);

END $$
DELIMITER ;

CALL Alter_Table();
DROP PROCEDURE Alter_Table;
