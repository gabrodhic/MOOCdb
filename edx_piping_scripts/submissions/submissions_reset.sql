-- WARNING: this query will delete all records from the table!

SET FOREIGN_KEY_CHECKS=0;
TRUNCATE moocdb.submissions;
ALTER TABLE moocdb.submissions AUTO_INCREMENT = 1;
SET FOREIGN_KEY_CHECKS=1;