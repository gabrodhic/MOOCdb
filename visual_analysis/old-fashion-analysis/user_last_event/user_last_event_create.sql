-- take 1 second to execute
-- Created on June 22, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

--
-- Table structure for table `user_last_event`
--

CREATE TABLE IF NOT EXISTS `user_last_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `resource_id` int(11) NOT NULL,
  `event_time` datetime NOT NULL,
  `duration` int(11) DEFAULT NULL,
  `source_br_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;