-- DELETE FROM moocdb.observed_events
-- WHERE observed_event_id >= 23000000;


SELECT max(source_br_id) FROM moocdb.observed_events;
-- SELECT source_br_id FROM moocdb.observed_events ORDER BY observed_event_id DESC LIMIT 1000;