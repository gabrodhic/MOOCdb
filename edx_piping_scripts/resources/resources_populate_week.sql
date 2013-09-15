-- Takes  seconds to execute
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- courseware

DROP PROCEDURE IF EXISTS find_resource_week;

DELIMITER $$
USE `moocdb`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `find_resource_week`()
begin

-- http://stackoverflow.com/questions/5125096/for-loop-in-mysql
declare v_max int unsigned default 20;
declare v_counter int unsigned default 0;

  start transaction;
  while v_counter < v_max do
    -- insert into foo (val) values ( floor(0 + (rand() * 65535)) );

	UPDATE moocdb.resources AS resources
	SET resources.resource_week  = v_counter
	WHERE LCASE(resources.resource_url) LIKE CONCAT('%/week_', v_counter, '/%'); 


    set v_counter=v_counter+1;
  end while;
  commit;
end$$

DELIMITER ;

CALL find_resource_week();