-- Takes 1881 seconds to execute
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- returned 5543 rows
INSERT INTO moocdb.resources (resource_name, resource_url, resource_type_id)
SELECT logs.br_logs.page, logs.br_logs.page, 0
FROM  logs.br_logs
GROUP BY logs.br_logs.page
ORDER BY logs.br_logs.page ASC;