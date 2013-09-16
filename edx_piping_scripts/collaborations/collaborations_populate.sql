-- take 5 seconds to execute
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
--
-- Modified on September 16, 2013 to add collaborations.source_post_id <franck.dernoncourt@gmail.com>

SET foreign_key_checks = 0;

TRUNCATE moocdb.collaborations;

-- Forum data
INSERT INTO moocdb.collaborations (user_id, collaboration_content, collaboration_timestamp, collaboration_parent_id, source_post_id)
SELECT askbot_post.author_id, askbot_post.text, askbot_post.added_at, 1, askbot_post.id
FROM forum_data.askbot_post AS askbot_post;
-- 	forum_data.auth_userprofile AS auth_userprofile
-- WHERE auth_userprofile.user_id = askbot_post.author_id;

-- Wiki data
INSERT INTO moocdb.collaborations (user_id, collaboration_content, collaboration_timestamp, collaboration_parent_id, source_post_id)
SELECT simplewiki_revision.revision_user_id, simplewiki_revision.contents, simplewiki_revision.revision_date, 2, simplewiki_revision.id
FROM forum_data.simplewiki_revision AS simplewiki_revision
;


SET foreign_key_checks = 1;