

-- ��root�û���¼ϵͳ��ִ�нű�


-- �������ݿ�
create database wechat character set utf8 ; 


-- ѡ�����ݿ�
use wechat;

-- ������

-- �����澯��Ϣ�� ����ֵ
DROP TABLE IF EXISTS `errinfo`;
CREATE TABLE `errinfo` (
  `touser` varchar(32) NOT NULL,
  `content` varchar(512) NOT NULL,
  `preInt` int(11) DEFAULT NULL,
  `preStr` varchar(128) DEFAULT NULL
)DEFAULT CHARSET=utf8;

commit;