# -*- coding: utf-8 -*-

import urllib2, json
import datetime
from dbProcess import dbProcess
import sys, os, time, datetime
import MySQLdb

class DoPostData(dbProcess):       
    def updateToken(self):
        try:
            reqUrl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (self.CorpId, self.Secrect)
            req = urllib2.urlopen(reqUrl)
            jsonData = json.load(req)
            jsonData.keys()
            access_token = jsonData['access_token'];
            leftTime  = jsonData['expires_in'];
            self.updateTime = time.time();
        except Exception as e:
            print ("postData fails {}".format(e));
            access_token = self.access_token
            leftTime = self.leftTime
        finally:
            print access_token      
            return access_token, leftTime
        
    def getToken(self):
        if self.leftTime < 500:
            self.access_token, self.leftTime = self.updateToken();
        else:
            self.leftTime = self.leftTime - (time.time() - self.updateTime);
            print 'leftTime: ', self.leftTime;
            print 'time.time():', time.time()
            print 'updateTime', self.updateTime;
        
    def postData(self, access_token, toUser, sendContent):
        try:
            postUrl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='  + access_token;
            
            jsonData = {"touser" : toUser, "toparty" : "", "totag" : "", "msgtype" : "text", "agentid" : self.AgentId, "text" : {"content" : sendContent, "safe":0}}
            #jsonData = {"touser" : 'hyp', "toparty" : "", "totag" : "", "msgtype" : "text", "agentid" : 1000002, "text" : {"content" : 'hello语法错误', "safe":0}};
            print jsonData;
            strData = json.dumps(jsonData)
            req = urllib2.urlopen(postUrl, strData)
            
            res = req.read()
            resJson = json.loads(res)
            resJson.keys()
            errCode = resJson['errcode']
            errMsg  = resJson['errmsg']
        except Exception as e:
            print ("postData fails {}".format(e));
            errCode = -999999;
            errMsg = 'postData fails...'
        finally:
            print 'errCode: ', errCode
            print 'errMsg: ', errMsg
            return errCode
        
    def doPost(self):
        selectSql = 'select * from errinfo';
        dbConn = MySQLdb.connect(host=self.IP, user=self.UserName, passwd=self.PassWord, db=self.DBName, charset='utf8');
        result = self.getData(selectSql, dbConn);
        print result;
        if not result:
            print "Table errinfo is empty.."
        else:
            for row in result:
                toUser = row[0];
                sendContent = row[1];
                rtnCode = self.postData(self.access_token, toUser, sendContent);
                if rtnCode != -999999:
                    sWhere = "touser = '%s'" % toUser;
                    dbConn = MySQLdb.connect(host=self.IP, user=self.UserName, passwd=self.PassWord, db=self.DBName, charset='utf8');
                    self.delData('errinfo', sWhere, dbConn);
        

if __name__ == '__main__':
        poster = DoPostData()
        while True:
            token = poster.getToken()
            poster.doPost()
            time.sleep(poster.Interval)