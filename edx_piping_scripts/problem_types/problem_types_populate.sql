
--
-- Dumping data for table `problem_types`
--

USE moocdb;

SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE problem_types;
SET FOREIGN_KEY_CHECKS=1;

INSERT INTO `problem_types` VALUES (0,'Unknown'),(1,'Homework'),(2,'Lecture quiz'),(3,'Lab'),(4,'Midterm example'),(5,'Midterm exam'), (6,'Final exam'), (7,'Sandbox');
