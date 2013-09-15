-- Takes 1 second
-- Created on June 30, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- courseware
UPDATE moocdb.resources 
SET resource_type_id=1
WHERE resource_url LIKE "%/courseware/%";

-- wiki
UPDATE moocdb.resources 
SET resource_type_id=2
WHERE resource_url LIKE "%/wiki/%";

-- book
UPDATE moocdb.resources 
SET resource_type_id=3
WHERE resource_url LIKE "%/book%";

-- profile
UPDATE moocdb.resources 
SET resource_type_id=4
WHERE resource_url LIKE "%/profile%";

-- problem
UPDATE moocdb.resources 
SET resource_type_id=5
WHERE resource_url LIKE "%/problem%";

-- tutorial
UPDATE moocdb.resources 
SET resource_type_id=7
WHERE resource_url LIKE "%/section%";

-- exercise
-- should be after section (tutorial)
UPDATE moocdb.resources 
SET resource_type_id=6
WHERE resource_url LIKE "%/exercise%";

-- exam
UPDATE moocdb.resources 
SET resource_type_id=8
WHERE resource_url LIKE "%[_]Exam%"; -- [_]: to  use the wildcard pattern matching characters as literal characters 
-- (http://stackoverflow.com/questions/5821/sql-server-2000-5-escape-an-underscore)

UPDATE moocdb.resources 
SET resource_type_id=8
WHERE lower(resource_url) LIKE "%exam%";


-- homework
UPDATE moocdb.resources 
SET resource_type_id=9
WHERE lower(resource_url) LIKE "%/homework%";

-- homework
UPDATE moocdb.resources 
SET resource_type_id=9
WHERE resource_url LIKE "%/exercise%";

-- information page
UPDATE moocdb.resources 
SET resource_type_id=10
WHERE resource_url LIKE "%mitx.mit.edu/info%";

-- extdeploy should be at the end
UPDATE moocdb.resources 
SET resource_type_id=19
WHERE resource_url LIKE "%https://extdeploy.mitx.mit.edu%";