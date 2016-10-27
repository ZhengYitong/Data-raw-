#coding:utf-8
__author__ = 'zhengyitong'

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import time
import MySQLdb
import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')




#database

class DBworker(object):

    def connectDB(self,hostName,userName,pwd,dbName):
        self.hostName=hostName
        self.userName=userName
        self.pwd=pwd
        self.dbName=dbName
        try:
            self.conn = MySQLdb.connect(host=hostName,user=userName,passwd=pwd,db=dbName,charset="utf8")
        except Exception, e:
            print e
            sys.exit()
        self.cursor=self.conn.cursor()
        #self.cursor.execute("SET NAMES utf8")
    def createTable(self):
        self.newsTableName="sinaNews_上海国际纺织展览 技术"

        try:
            self.cursor.execute('''

CREATE TABLE IF NOT exists `'''+self.newsTableName+'''` (
  `Id` int(11) NOT NULL auto_increment,
  `News` varchar(255) default NULL,
  `Datetime`varchar(255) default NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

''')
        except Exception, e:
            print e


        print "CREATE TABLES\n"

    #insert data
    def insertProject(self,news,datetime):
        try:
            self.cursor.execute("insert into`"+self.newsTableName+"`(`News`,`Datetime`) values('%s','%s')"\
                                %(news,datetime))

        except Exception, e:
            print e

        try:
            self.conn.commit()
        except Exception, e:
            print e
            self.closeDB()
            self.connectDB(self.hostName,self.userName,self.pwd,self.dbName)

    #close database
    def closeDB(self):
        self.cursor.close()
        self.conn.close()

   #raw data
class newsWorker(object):
    db=DBworker()


    def createTable(self,hostName,userName,pwd,dbName):
        self.db.connectDB(hostName,userName,pwd,dbName)
        self.db.createTable()
        #self.db.closeDB()

    def connectDB(self,hostName,userName,pwd,dbName):
        self.db.connectDB(hostName,userName,pwd,dbName)

    def closeDB(self):
        self.db.closeDB()

    #def enter(self):





    #def getNews(self):




if __name__=='__main__':

    #q=raw_input("please input keyword:")
    #print q
    #r= urllib.quote(q)
    a=newsWorker()
    a.db.connectDB("127.0.0.1","root","sinweetyYI316","sinaNews")
    a.createTable("127.0.0.1","root","sinweetyYI316","sinaNews")
    url="http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs=%E4%B8%8A%E6%B5%B7%E5%9B%BD%E9%99%85%E7%BA%BA%E7%BB%87%E5%B1%95%E8%A7%88+%E6%8A%80%E6%9C%AF&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E4%B8%8A%E6%B5%B7%E5%9B%BD%E9%99%85%E7%BA%BA%E7%BB%87%E5%B1%95%E8%A7%88+%E6%8A%80%E6%9C%AF&rsv_sug3=1&rsv_sug4=31&rsv_sug1=1&rsv_sug2=0&inputT=4&rsv_sug=1"
    browser = webdriver.Chrome()
    browser.get(url)

    for pagenum in range(1,5):
        elem=browser.find_element_by_xpath("//div[@id='content_left']")
        newss=elem.find_elements_by_xpath("//div[@class='result']")
        datetimes=elem.find_elements_by_xpath("//p[@class='c-author']")


        for i in range(0,len(newss)):
            #for date in datetimes:
            datetime=datetimes[i].text

            #for new in newss:

            news=newss[i].text

            a.db.insertProject(news,datetime)

        click=browser.find_element_by_id("page")
        click.find_element_by_xpath("//a[@class='n']").click()

    a.db.closeDB()

    print "FINISHED: ",'over'


