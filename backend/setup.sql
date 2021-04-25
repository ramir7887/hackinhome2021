use hackinhome;
CREATE TABLE `appeal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` int(11) DEFAULT NULL,
  `message_id` int(11) DEFAULT NULL,
  `text` varchar(1000) DEFAULT NULL,
  `departament_id` int(11) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) 

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` int(14) DEFAULT NULL,
  `stud_id` int(11) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) 


CREATE TABLE `departaments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `departament_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) 


CREATE TABLE `user_type` (
  `id` int(11) NOT NULL,
  `type_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) 
