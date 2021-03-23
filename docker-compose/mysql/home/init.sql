use retail001;

CREATE TABLE `profit_rate` (
  `level` TINYINT(2) PRIMARY KEY NOT NULL,
  `rate`  FLOAT(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `retail_info` (
  `legal_person` CHAR(16) NOT NULL,
  `retail_name`  CHAR(32) NOT NULL,
  `retail_type`  CHAR(16) NOT NULL,
  `retail_address` CHAR(64),
  `phone_number` char(20)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `native_user` (
  `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
  `uid` CHAR(60) UNIQUE NOT NULL ,
  `username` CHAR(32) UNIQUE NOT NULL ,
  `password` CHAR(120) NOT NULL,
  `active` TINYINT(1) NOT NULL,
  `phone_number` char(20),
  `create_time` DATETIME NOT NULL,
  `update_time` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `external_user` (
  `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
  `uid` CHAR(60) NOT NULL UNIQUE,
  `account_source` TINYINT(2) NOT NULL, 
  `create_time` DATETIME NOT NULL,
  `update_time` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user_profile` (
  `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
  `nickname` CHAR(32) UNIQUE NOT NULL,
  `picture_link` VARCHAR(32), 
  `account_level` TINYINT(2),
  `gender` TINYINT(1),
  `whatsup` VARCHAR(480),  
  `name` CHAR(32),
  `email` CHAR(64),
  `NAID` INT(11),
  `EAID` INT(11),
  CONSTRAINT `fk_NAID_from_native_user`
  FOREIGN KEY(`NAID`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `fk__EAID_from_external_user`
  FOREIGN KEY(`EAID`) REFERENCES `user_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `account_capital` (
  `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
  `profile_id` INT(11) UNIQUE,
  `balance`  INT NOT NULL,
  `member_point` INT NOT NULL,
  CONSTRAINT `fk__capital_profile_id_from_user_profile`
  FOREIGN KEY(`profile_id`) REFERENCES `user_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `promote_generation` (
  id INT(11) PRIMARY KEY NOT NULL,
  `promotee_id` INT(11) NOT NULL UNIQUE,
  `promoter_level1_id` INT(11), 
  `promoter_level2_id` INT(11),
  `promoter_level3_id` INT(11),
  CONSTRAINT `fk_promotee_id_from_account_profile`
  FOREIGN KEY(`promotee_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `fk_promoter_level1_id_from_user_profile`
  FOREIGN KEY(`promoter_level1_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `fk_promoter_level2_id_from_user_profile`
  FOREIGN KEY(`promoter_level2_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `fk_promoter_level3_id_from_user_profile`
  FOREIGN KEY(`promoter_level3_id`) REFERENCES `user_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO profit_rate (level,rate) VALUES (1,0.03);
INSERT INTO profit_rate (level,rate) VALUES (2,0.05);
INSERT INTO profit_rate (level,rate) VALUES (3,0.10);
INSERT INTO profit_rate (level,rate) VALUES (99,0.00);


INSERT INTO retail_info (legal_person,retail_name,retail_type,retail_address) 
    VALUES("黄鹤"," 江南皮革厂"," 皮革厂","江南");



INSERT INTO native_user (
  uid,username,password,phone_number,active,create_time,update_time)
    VALUES("abc","jiangnan","jiangbei","15755555555",1,now(),now());

INSERT INTO native_user (
  uid,username,password,phone_number,active,create_time,update_time)
    VALUES("adsk","jiangbei","jiangbei","157555566666",1,now(),now());

INSERT INTO user_profile (
  nickname,picture_link,gender,name,NAID)
    VALUES("江南","http://1",1,"黄江南",1);

INSERT INTO user_profile (
  nickname,picture_link,gender,name,NAID)
    VALUES("江北1","http://2",1,"江北",2);


INSERT INTO account_capital (
  profile_id,balance,member_point)
    VALUES(1,10000,10000)
