-- Takes 5 seconds to execute
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Careful, on Unix you need to replace by "'\r'" instead of "'\n'".
LOAD DATA LOCAL INFILE 'C:\\programming\\evo\\svn3\\EDXDataMining\\Franck\\database\\ip\\GeoIPCountryWhois.csv' 
INTO TABLE moocdb.ip_country FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
