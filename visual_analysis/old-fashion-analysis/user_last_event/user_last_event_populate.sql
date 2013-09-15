-- Takes 30371 seconds to executes (when passive is 6 GB and 130,000,000 rows)
-- MySQL read 1.5 TB on the drive
-- Only takes 200 seconds when innodb_buffer_pool_size is set at 5 GB
-- Created on June 22, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

INSERT INTO moocdb.user_last_event (user_id, resource_id, event_time, duration, source_br_id)
	SELECT observed_events.user_id, observed_events.resource_id, 
			max(observed_events.observed_event_timestamp), observed_events.observed_event_duration, observed_events.source_br_id
	FROM moocdb.observed_events AS observed_events
	GROUP BY observed_events.user_id
;