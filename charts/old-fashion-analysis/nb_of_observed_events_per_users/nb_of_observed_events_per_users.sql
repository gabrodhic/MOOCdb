SELECT count(*) AS count 
FROM edx.passive
WHERE user_id IS NOT NULL 
GROUP BY user_id 
ORDER BY count DESC;