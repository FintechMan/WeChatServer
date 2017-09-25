

-- 用root用户登录系统，执行脚本


-- 创建数据库
create database wechat character set utf8 ; 


-- 选择数据库
use wechat;

-- 创建表

-- 创建告警信息表 并赋值
DROP TABLE IF EXISTS `errinfo`;
CREATE TABLE `errinfo` (
  `touser` varchar(32) NOT NULL,
  `content` varchar(512) NOT NULL,
  `preInt` int(11) DEFAULT NULL,
  `preStr` varchar(128) DEFAULT NULL
)DEFAULT CHARSET=utf8;

commit;