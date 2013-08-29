-- Takes 5 seconds to run
SELECT problem_id, COUNT(*) AS count FROM moocdb.submissions2 GROUP BY problem_id ORDER BY count DESC;cd 