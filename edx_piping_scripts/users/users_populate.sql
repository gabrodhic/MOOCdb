INSERT INTO moocdb.users (user_id, user_name)
SELECT auth_user.id, auth_user.username
FROM forum_data.auth_user as auth_user
ORDER BY auth_user.id;