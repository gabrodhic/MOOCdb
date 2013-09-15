-- Takes 60 seconds
-- Created on June 25, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- http://dev.mysql.com/doc/refman/5.0/en/miscellaneous-functions.html#function_inet-aton

UPDATE moocdb.users as users
SET user_ip = (
	SELECT INET_ATON(br_logs.ip) 
	FROM logs.br_logs AS br_logs
	WHERE br_logs.username = users.user_name
	LIMIT 1
)

;