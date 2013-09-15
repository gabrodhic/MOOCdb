-- Takes  seconds to execute
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
SELECT observed_events.resource_id
FROM  moocdb.resources AS resources
 INNER JOIN moocdb.observed_events AS observed_events
 ON observed_events.resource_id = resources.resource_id
WHERE observed_events.observed_event_timestamp = (
	SELECT MIN(observed_events.resource_id)
	FROM  moocdb.observed_events AS observed_events2
	WHERE observed_events2.resource_id = observed_events.resource_id
)
LIMIT 10
;
