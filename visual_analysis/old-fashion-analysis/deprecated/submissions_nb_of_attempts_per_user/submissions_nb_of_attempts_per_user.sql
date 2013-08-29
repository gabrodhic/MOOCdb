-- Takes 5 seconds to run
SELECT COUNT(*) AS count FROM moocdb.submissions2 GROUP BY user_id ORDER BY count DESC;