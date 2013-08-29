SELECT users.user_country, COUNT(*) AS count
FROM moocdb.users AS users
WHERE users.user_final_grade >= 0.5
GROUP BY users.user_country
ORDER BY count DESC;