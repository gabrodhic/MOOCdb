-- take 5 seconds to execute
-- Created on July 2, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT LENGTH(collaborations.collaboration_content) 
FROM moocdb.collaborations AS collaborations
ORDER BY LENGTH(collaborations.collaboration_content) DESC ;

