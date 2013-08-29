-- Takes 5 seconds to execute
SELECT DATEDIFF(collaborations.collaboration_timestamp, '2012-03-03 00:00:01') AS day, COUNT(*) AS count
FROM moocdb.collaborations AS collaborations
WHERE collaborations.collaboration_parent_id = 1
GROUP BY day
ORDER BY day ASC ;

