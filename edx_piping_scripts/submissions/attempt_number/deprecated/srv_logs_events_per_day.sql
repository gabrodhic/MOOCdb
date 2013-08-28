-- Takes 50 seconds to execute
SELECT DATEDIFF(time, '2012-03-03 00:00:01') AS day, COUNT(*) AS count
FROM logs2.srv_logs 
GROUP BY day
ORDER BY day ASC ;

