-- Takes 0 second
-- Created on June 18, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

--
-- Dumping data for table `problem_types`
--

USE moocdb;

SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE problem_types;
SET FOREIGN_KEY_CHECKS=1;

INSERT INTO `problem_types` VALUES (0,'Unknown'),(1,'Homework'),(2,'Lecture quiz'),(3,'Lab'),(4,'Midterm example'),(5,'Midterm exam'), (6,'Final exam'), (7,'Sandbox');
