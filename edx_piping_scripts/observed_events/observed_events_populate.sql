-- Takes 30 seconds for 1,000,000 rows in browser logs, so since the latter has around 130,000,000 this script will take around 3600 seconds,
-- Created on June 10, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- WARNING: add index on resources.location and users.username

INSERT INTO moocdb.observed_events (user_id, resource_id, observed_event_timestamp, observed_event_duration, source_br_id)
SELECT users.user_id, resources.resource_id, br_logs.time, 0, br_logs.id
FROM moocdb.users as users, logs.br_logs as br_logs, moocdb.resources as resources
WHERE br_logs.username = users.user_name
AND br_logs.page = resources.resource_url
AND br_logs.id >= 1000000
AND br_logs.id < 40000000;
--            10,000,000