-- Takes 20 seconds to execute
-- Created on Jun 27, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

DROP PROCEDURE IF EXISTS Alter_Table;

DELIMITER $$
CREATE PROCEDURE Alter_Table()
BEGIN

	DECLARE _count INT;

	SET _count = (  SELECT COUNT(*) 
						FROM INFORMATION_SCHEMA.COLUMNS
						WHERE   TABLE_SCHEMA = 'moocdb' AND
								TABLE_NAME = 'users' AND 
								COLUMN_NAME = 'user_submissions_count');

	IF _count = 0 THEN
		ALTER TABLE `moocdb`.`users` 
			ADD COLUMN `user_submissions_count` INT(11) NULL;
	END IF;

	UPDATE moocdb.users AS users
		SET users.user_submissions_count = (
			SELECT 
				 COUNT(*) 
			FROM
				moocdb.submissions AS submissions
			WHERE
				submissions.user_id = users.user_id
		);


END $$
DELIMITER ;

CALL Alter_Table();
DROP PROCEDURE IF EXISTS Alter_Table;
