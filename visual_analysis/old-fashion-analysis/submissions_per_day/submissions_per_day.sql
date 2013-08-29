-- Takes 12 seconds to run
SELECT DATEDIFF(submissions.submission_timestamp, '2012-03-03 00:00:01') AS day, COUNT(*) AS count
FROM moocdb.submissions2 AS submissions
GROUP BY day 
ORDER BY day ASC;
