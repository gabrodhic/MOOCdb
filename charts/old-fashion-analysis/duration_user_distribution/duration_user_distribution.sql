-- duration_user_distribution.sql
-- Takes 2000 seconds to execute
SELECT 
	COUNT(*) AS occurrences, 
	MIN(observed_events.observed_event_duration),
	MAX(observed_events.observed_event_duration),
	AVG(observed_events.observed_event_duration),
	STD(observed_events.observed_event_duration),
	SUM(observed_events.observed_event_duration)
	
FROM moocdb.observed_events AS observed_events,
	 moocdb.users AS users
WHERE observed_events.user_id = users.user_id
GROUP BY users.user_id
ORDER BY SUM(observed_events.observed_event_duration) DESC
;