CREATE DATABASE  IF NOT EXISTS `mock` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mock`;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(30) DEFAULT NULL,
  `user_gender` tinyint(4) DEFAULT NULL,
  `user_birthdate` date DEFAULT NULL,
  `user_country` varchar(3) DEFAULT NULL,
  `user_ip` int(10) unsigned DEFAULT NULL,
  `user_timezone_offset` int(11) DEFAULT NULL,
  `user_final_grade` double DEFAULT NULL,
  `user_join_timestamp` datetime DEFAULT NULL,
  `user_os` int(11) DEFAULT NULL,
  `user_agent` int(11) DEFAULT NULL,
  `user_language` int(11) DEFAULT NULL,
  `user_screen_resolution` varchar(45) DEFAULT NULL,
  `user_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

DROP PROCEDURE IF EXISTS LOAD_USERS;

DELIMITER $$
CREATE PROCEDURE LOAD_USERS()
   BEGIN      
    DECLARE a INT Default 0;
    START transaction;
          simple_loop: LOOP
             SET a=a+1;
             select a;
             INSERT INTO `users` VALUES (a, NULL, NULL, NULL, NULL,  NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
             IF a=50 THEN
                LEAVE simple_loop;
             END IF;
          END LOOP simple_loop;
    commit;
END $$

CALL LOAD_USERS();

