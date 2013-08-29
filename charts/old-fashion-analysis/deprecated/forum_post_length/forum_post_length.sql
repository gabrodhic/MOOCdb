-- Takes 5 seconds to execute
SELECT LENGTH(collaborations.collaboration_content) 
FROM moocdb.collaborations AS collaborations
ORDER BY LENGTH(collaborations.collaboration_content) DESC ;

