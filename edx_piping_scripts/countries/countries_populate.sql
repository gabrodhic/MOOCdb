-- Takes a 1 second to execute
-- Created on June 18, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Be careful, on Mac you need to change "'\n'" into "'\r'"
LOAD DATA LOCAL INFILE 'C:\\programming\\evo\\svn3\\EDXDataMining\\MOOCdb\\creation\\countries\\country_population.csv' 
INTO TABLE moocdb.countries FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
