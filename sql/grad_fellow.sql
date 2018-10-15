DROP TABLE IF EXISTS `country`;

CREATE TABLE `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;

INSERT INTO `country` (`id`, `name`)
VALUES
	(1,'China'),
	(2,'India'),
	(4,'Japan'),
	(3,'Korean');

/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `position`;

CREATE TABLE `position` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `position` WRITE;
/*!40000 ALTER TABLE `position` DISABLE KEYS */;

INSERT INTO `position` (`id`, `name`)
VALUES
	(2,'Business Analyst'),
	(4,'Network Engineer'),
	(1,'Software EngineerSystem Analyst'),
	(7,'Software Test'),
	(5,'Technical Consultant'),
	(3,'Technical support'),
	(6,'Web Developer');

/*!40000 ALTER TABLE `position` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `user_info`;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;

INSERT INTO `user` (`id`, `name`, `password`)
VALUES
	(1,'test','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(2,'test2','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(3,'test3','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(4,'test4','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(5,'test5','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(6,'test6','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(7,'test7','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(8,'test8','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(9,'test9','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(10,'test10','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(11,'test11','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f'),
	(12,'test12','pbkdf2:sha256:50000$GBkQyeoQ$4bdfb7d0d22da3dc41153707e054b2054afd5c1c624e54476e9523b3a8f1c20f');
/* password: 123456 */

/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;



CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `position` varchar(100) NOT NULL,
  `company` varchar(100) DEFAULT NULL,
  `nationality` varchar(100) NOT NULL,
  `tobe_contacted` tinyint(1) DEFAULT NULL,
  `skills_have` text,
  `skills_learned` text,
  `skills_recommend` text,
  `skills_roles_in_company` text,
  `skills_tasks_auto` text,
  `skills_tasks_collab` text,
  `cc_competitiveness` text,
  `cc_desc_by_colleagues` text,
  `cc_working_approach` text,
  `cc_relationship_with_colleague` text,
  `cc_relationship_with_mgr` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `user_info_ibfk_1` FOREIGN KEY (`name`) REFERENCES `user` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;

INSERT INTO `user_info` (`id`, `name`, `first_name`, `last_name`, `position`, `company`, `nationality`, `tobe_contacted`, `skills_have`, `skills_learned`, `skills_recommend`, `skills_roles_in_company`, `skills_tasks_auto`, `skills_tasks_collab`, `cc_competitiveness`, `cc_desc_by_colleagues`, `cc_working_approach`, `cc_relationship_with_colleague`, `cc_relationship_with_mgr`)
VALUES
  (1,'test','Huang','Xiao','Business Analyst','Global Consulting Services','China',1,'3months Python Subject','Advanced Python through on-job training','Business Process Modeling','Product Owner, Technical lead, User Experience Designer, Quality Assurance','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further'),
  (2,'test2','Yong','Wu','Business Analyst','REA','China',0,'3 months Datawarehousing','Project management skill','Business process modelling','Product Owner, Technical lead, User Experience Designer','monthly measurement report','product presentation with product owner','salary','caring','flexible','we exchange news when having lunch together','He made me feel being trusted'),
  (3,'test3','Hua','Li','Software Test','REA','Japan',1,'3 months Datawarehousing','Project management skill','Business process modelling','Product Owner, Technical lead, User Experience Designer','monthly measurement report','product presentation with product owner','salary','caring','flexible','we exchange news when having lunch together','He made me feel being trusted'),
  (4,'test4','Yan','Wu','Web Developer','Sevian','China',1,'3 months Javascript','VUE JS on the job','Human Interaction Design','Product Owner, Technical lead, User Experience Designer','front end develop','team meeting with product owner','salary','smart','customer-centered','we have lunch together','He encouraged me a lot'),
  (5,'test5','Aarav','Sakthi','System Analyst','KPMG','India',1,'3 months Python subject','SQL in Uni','Enterprise Architecture','Product Owner, Technical lead','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further'),
  (6,'test6','Keiko','Ranmaru','Technical Support','Lancom','Japan',1,'3 months Programming Basics','Project management skill','Business process modelling','Product Owner, Technical lead, User Experience Designer','monthly measurement report','product presentation with product owner','salary','caring','flexible','we exchange news when having lunch together','He made me feel being trusted'),
  (7,'test7','Yun','Zhang','Business Analyst','ANZ','China',1,'3months Python Subject','Advanced Python through on-job training','Business Process Modeling','Product Owner, Technical lead, User Experience Designer, Quality Assurance','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further'),
  (8,'test8','Eun Ae','Pak','Software Engineer','Pearson','Korean',1,'3months Agorithm Subject','Advanced Python through on-job training','Enterprise Architecture','Product Owner, Technical lead, User Experience Designer','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further'),
  (9,'test9','Min','Zheng','Business Analyst','KPMG','China',1,'3months Python Subject','Advanced Python through on-job training','Business Process Modeling','Product Owner, Technical lead, User Experience Designer, Quality Assurance','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further'),
  (10,'test10','Yancen','Wu','Business Analyst','ANZ','China',1,'3months Python Subject','Enterprise Architecture','Business Process Modeling','Product Owner, Technical lead, User Experience Designer, Quality Assurance','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further'),
  (11,'test11','Jieming','Li','Business Analyst','Microsoft','China',1,'3months Python Subject','Javascript on-job training','Business Process Modeling','Product Owner, Technical lead, User Experience Designer, Quality Assurance','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further'),
  (12,'test12','Can','Zhang','Business Analyst','EY','China',1,'3months SQL','Human centered design course','Business Process Modeling','Product Owner, Technical lead, User Experience Designer','Analyse competitor\'s products','Stand-up meeting with development team','Salary, Welfare','caring, pay attention to details','agile','colleagues are friendly and fun','My manager listens to my view and guides me to explore further');
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;
