-- Takes 40 seconds for one iteration
-- Created on June 18, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- Create INDEX on active.source_cw_id
drop procedure if exists load_attempts;

delimiter #

create procedure load_attempts()
begin

-- http://stackoverflow.com/questions/5125096/for-loop-in-mysql
declare v_max int unsigned default 200;
declare v_counter int unsigned default 0;

  -- start transaction;
  while v_counter < v_max do
    -- insert into foo (val) values ( floor(0 + (rand() * 65535)) );

	-- Takes 30 seconds for 1,000,000 rows in browser logs, so since the latter has around 130,000,000 this script will take around 3600 seconds,
	-- WARNING: add index on resources.location and users.username
	INSERT INTO moocdb.observed_events (user_id, resource_id, observed_event_timestamp, observed_event_duration, source_br_id)
	SELECT users.user_id, resources.resource_id, br_logs.time, 0, br_logs.id
	FROM moocdb.users as users, logs.br_logs as br_logs, moocdb.resources as resources
	WHERE br_logs.username = users.user_name
	AND br_logs.page = resources.resource_url
	AND br_logs.id >= (v_counter *1000000)
	AND br_logs.id < ((v_counter + 1) *1000000);
	--                               10,000,000 


    set v_counter=v_counter+1;
  end while;
  -- commit;
end #

delimiter ;

call load_attempts();
drop procedure if exists load_attempts();