-- duration_per_grade.sql
-- Takes 900 seconds to execute
SELECT letter_grade.grade,
	(COUNT(*) / letter_grade.number_of_students) AS occurrences,
	MIN(observed_events.observed_event_duration),
	MAX(observed_events.observed_event_duration),
	AVG(observed_events.observed_event_duration),
	STD(observed_events.observed_event_duration),
	SUM(observed_events.observed_event_duration) / letter_grade.number_of_students
	
FROM moocdb.observed_events AS observed_events,
	 moocdb.users AS users,
	moocdb.letter_grade AS letter_grade
WHERE observed_events.user_id = users.user_id
	AND letter_grade.grade = users.user_final_grade
GROUP BY letter_grade.grade
ORDER BY SUM(observed_events.observed_event_duration) DESC
;
