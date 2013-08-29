-- Takes 1000 seconds to execute
SELECT resources.resource_name,
	COUNT(*) AS occurrences, 
	MIN(observed_events.observed_event_duration),
	MAX(observed_events.observed_event_duration),
	AVG(observed_events.observed_event_duration),
	STD(observed_events.observed_event_duration),
	SUM(observed_events.observed_event_duration)
FROM moocdb.observed_events AS observed_events,
	 moocdb.resources AS resources
WHERE observed_events.resource_id = resources.resource_id
GROUP BY resources.resource_id
ORDER BY occurrences DESC
;