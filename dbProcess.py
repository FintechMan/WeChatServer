# -*- coding: utf-8 -*-

import ConfigParser
import logging
import datetime,time
import os, sys
import MySQLdb

class dbProcess(object):
    def __init__(self):
        print "dbProcess __init__";

        print "get MySQL Information from file: %s\n" % 'C:\\test\\company\\wechat.cnf'
        mysqlConfig = ConfigParser.ConfigParser();
        mysqlConfig.read("C:\\test\\company\\wechat.cnf");
        self.IP = mysqlConfig.get("MYSQL", "IP");
        self.UserName = mysqlConfig.get("MYSQL", "UserName");
        self.PassWord = mysqlConfig.get("MYSQL", "PassWord");
        self.DBName = mysqlConfig.get("MYSQL", "DBName");
        #self.conn = MySQLdb.connect(host=self.IP, user=self.UserName, passwd=self.PassWord, db=self.DBName, charset='utf8');
        
        print "get App Information from file: %s\n" % 'C:\\test\\company\\wechat.cnf'
        self.CorpId = mysqlConfig.get("APP", "corpId");
        self.Secrect = mysqlConfig.get("APP", "secrect");
        self.AgentId = mysqlConfig.get("APP", "agentid");
        self.Interval = float(mysqlConfig.get("APP", "interval"));
        self.leftTime  = 0;
        
    def isset(self,v):
        try:
            type (eval(v))
        except:
            return False
        else:
            return True
        
    def getData(self, sSelectSql, conn):
        print 'SelectSql: ', sSelectSql;
        try:
            cursor = conn.cursor();
            cursor.execute(sSelectSql);
            allData = cursor.fetchall();
            #print allData[0][0];
        except Exception as e:
            print ("select data fails {}".format(e));
            allData = ();
        finally:
            if self.isset("cursor"):
                cursor.close();
            if self.isset("conn"):
                conn.close();
        return allData;
                
    def delData(self, sTableName, sWhere, conn):
        delSQL = "delete from %s where %s" % (sTableName, sWhere);
        print delSQL;
        try:
            cursor = conn.cursor();
            cursor.execute(delSQL);
            conn.commit();
        except Exception as e:
            print ("delete data fails {}".format(e));
        finally:
            if self.isset("cursor"):
                cursor.close();
            if self.isset("conn"):
                conn.close();
        
        
if __name__=="__main__":
    dbProcesser = dbProcess();
    sSelectSql = 'select * from errinfo';
    dbProcesser.getData(sSelectSql);
    sTableName = 'errinfo'
    sWhere = "touser = 'hyp'"
    dbProcesser.delData(sTableName, sWhere)