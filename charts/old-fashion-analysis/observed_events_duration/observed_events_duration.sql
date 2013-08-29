-- Takes 1100 seconds to execute

SELECT resource_types.resource_type_name, 
	count(*) as occurrences, 
	MIN(observed_events.observed_event_duration),
	MAX(observed_events.observed_event_duration),
	AVG(observed_events.observed_event_duration),
	STD(observed_events.observed_event_duration),
	SUM(observed_events.observed_event_duration)
FROM moocdb.observed_events AS observed_events,
	 moocdb.resource_types AS resource_types,
	 moocdb.resources AS resources
WHERE observed_events.resource_id = resources.resource_id
	AND resources.resource_type_id = resource_types.resource_type_id
GROUP BY resource_types.resource_type_id
ORDER BY resource_types.resource_type_name
;
