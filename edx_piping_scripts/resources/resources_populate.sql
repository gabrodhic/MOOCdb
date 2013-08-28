-- took 1881 seconds to execute
-- returned 5543 rows
INSERT INTO moocdb.resources (resource_name, resource_url, resource_type_id)
SELECT logs.br_logs.page, logs.br_logs.page, 0
FROM  logs.br_logs
GROUP BY logs.br_logs.page
ORDER BY logs.br_logs.page ASC;