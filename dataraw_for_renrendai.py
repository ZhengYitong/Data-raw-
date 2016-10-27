__author__ = 'zhengyitong'

#encoding=utf-8
# -*- coding: utf-8 -*-

import re
import urllib2
import MySQLdb
import urllib
import sys
import cookielib

reload(sys)
sys.setdefaultencoding('utf-8')



def getHTML(url, time = 0):
    try:
        html = urllib2.urlopen(url).read()
    except Exception, e:
        print e
        print "=== Connecting again..."

        if time==3:
            return -1
        time += 1
        html=getHTML(url, time)
    return html


#loginTry
def getloginHTML(pageurl):
    data={"j_username":"13261708330",
          "j_password":"zhengYI316"}
    post_data=urllib.urlencode(data)

    loginurl="https://www.we.com/j_spring_security_check"

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')]
    urllib2.install_opener(opener)


    req = urllib2.Request(loginurl,post_data)
    _response = urllib2.urlopen(req)
    _d=_response.read()
    _d =_d.decode("utf-8")
    y=_d



    req2=urllib2.Request(pageurl)
    _response2=urllib2.urlopen(req2)
    _d2=_response2.read()
    _d2 =_d2.decode("utf-8")
    return _d2


class loginTry:
    post_data=""
    def __init__(self):

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')]
        urllib2.install_opener(opener)

    def login(self,loginurl,bianma):

        req = urllib2.Request(loginurl,self.post_data)
        _response = urllib2.urlopen(req)
        _d=_response.read()
        _d =_d.decode(bianma)
        return _d

    def getpagehtml(self,pageurl,bianma):

        req2=urllib2.Request(pageurl)
        _response2=urllib2.urlopen(req2)
        _d2=_response2.read()
        _d2 =_d2.decode(bianma)
        return _d2

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
        self.threadTableName="loanList_160409"
        self.userTableName="borrower_160409"
        self.lenderTableName="lender_160409"

        try:
            self.cursor.execute('''

CREATE TABLE IF NOT exists `'''+self.threadTableName+'''` (
  `loanId` int(11) NOT NULL auto_increment,
  `title` varchar(255) default NULL,
  `status` varchar(255) default NULL,
  `rate` varchar(255) default NULL,
  `interest` varchar(255) default NULL,
  `borrowerId` varchar(255) default NULL,
  `nickName` varchar(255) default NULL,
  `borrowerType` varchar(255) default NULL,
  PRIMARY KEY  (`loanId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

''')
        except Exception, e:
            print e
        try:
            self.cursor.execute('''
CREATE TABLE IF NOT exists `'''+self.userTableName+'''` (
  `Id` varchar(100) NOT NULL default '',
  `userName` varchar(255) default NULL,
  `borrowerLevel` varchar(255) default NULL,
  `address` varchar(255) default NULL,
  `jobType` varchar(255) default NULL,
  `verifyState` varchar(255) default NULL,
  `marriage` varchar(255) default NULL,
  `age` varchar(255) default NULL,
  `education` varchar(255) default NULL,
  `income` varchar(255) default NULL,
  `house` varchar(255) default NULL,
  `car` varchar(255) default NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


''')
        except Exception, e:
            print e

        try:
            self.cursor.execute('''
CREATE TABLE IF NOT exists `'''+self.lenderTableName+'''` (
  `Id` varchar(100) NOT NULL default '',
  `userId` varchar(255) default NULL,
  `userName` varchar(255) default NULL,
  `loanId` varchar(255) default NULL,
  `tradeMethod` varchar(11) default NULL,
  `amount` varchar(11) default NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


''')
        except Exception, e:
            print e



        print "CREATE TABLES\n"

    #create table using mysqlworkbench




    #insert project
    def insertProject(self,proid,proname,prorate,prostatus,promoney,borrowerId,nickName,borrowerType):
        try:
            self.cursor.execute("insert into`"+self.threadTableName+"`(`loanId`,`title`,`rate`,`status`,`interest`,`borrowerId`,`nickName`,`borrowerType`) values(%d,'%s','%s','%s','%s','%s','%s','%s')"\
                                %(int(proid),proname,prorate,prostatus,promoney,borrowerId,nickName,borrowerType))

        except Exception, e:
            print e

        try:
            self.conn.commit()
        except Exception, e:
            print e
            self.closeDB()
            self.connectDB(self.hostName,self.userName,self.pwd,self.dbName)

    #insert user
    def insertBorrowerInfo(self,userid,name,level,address,job,verify,ma,age,edu,income,house,car):
        try:
            self.cursor.execute("insert into `"+self.userTableName+"`(`Id`,`userName`,`borrowerLevel`,`address`,`jobType`,`verifyState`,`marriage`,`age`,`education`,`income`,`house`,`car`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                                %(userid,name,level,address,job,verify,ma,age,edu,income,house,car))
        except Exception, e:
            print e
        self.conn.commit()

    def insertLenderInfo(self,userid,id,proid,name,method,amount):
        try:
            self.cursor.execute("insert into `"+self.lenderTableName+"`(`Id`,`userId`,`userName`,`loanId`,`tradeMethod`,`amount`) values('%s','%s','%s','%s','%s','%s')"\
                                %(id,userid,name,proid,method,amount))
        except Exception, e:
            print e
        self.conn.commit()

    #check user in database
    def checkUser(self,userid):
        try:
            self.cursor.execute("select count(*) from `"+self.userTableName+"`where Id=`"+str(userid)+"`")
            result=self.cursor.fetchall()
        except Exception,e:
            print e

        #self.conn.commit()
        return result[0][0]
    def checkLoan(self,proid):
        try:
            self.cursor.execute("select count(*) from `"+self.threadTableName+"`where loanId=`"+str(proid)+"`")
            result=self.cursor.fetchall()
        except Exception,e:
            print e

        #self.conn.commit()
        return result[0][0]


    #close database
    def closeDB(self):
        self.cursor.close()
        self.conn.close()


class renrendaiWorker(object):
    db=DBworker()


    def createTable(self,hostName,userName,pwd,dbName):
        self.db.connectDB(hostName,userName,pwd,dbName)
        self.db.createTable()
        #self.db.closeDB()

    def connectDB(self,hostName,userName,pwd,dbName):
        self.db.connectDB(hostName,userName,pwd,dbName)

    def closeDB(self):
        self.db.closeDB()



         #listpage--sum
    def getIndex(self,page):
        global  bbid,bt,bl,add,jt,vy,ma
        url="http://www.we.com/lend/loanList!json.action?pageIndex="+str(page)
        #print url
        indexPage=getHTML(url)
        #print indexPage
        indexPage=re.sub("\n","",indexPage)
        #titleBlockPat=re.compile(r'".*?":[^,]*,')
        #titleBlocks=titleBlockPat.findall(indexPage)

        proidPat=re.compile('"loanId":[^,]*,')
        prostPat=re.compile('"status":"[^,]*,')
        pronPat=re.compile('"title":"[^,]*,')
        promPat=re.compile('"amount":[^,]*,')
        prorPat=re.compile('"interest":[^,]*,')
        #uidPat=re.compile('"borrowerId":[^,]*,')

        if(len(indexPage)>0):
            proids=proidPat.findall(indexPage)
            prosts=prostPat.findall(indexPage)
            pronas=pronPat.findall(indexPage)
            proms=promPat.findall(indexPage)
            prors=prorPat.findall(indexPage)
            #uids=uidPat.findall(indexPage)

            for i in range(0,len(proids)):
                try:
                    pid=re.sub(r'loanId|"|:|.0|,',"",proids[i])
                    #print pid
                    ps=re.sub(r'status|"|:|,',"",prosts[i])
                    pn=re.sub(r'title|"|:|,',"",pronas[i])
                    pm=re.sub(r'amount|"|:|,',"",proms[i])
                    pr=re.sub(r'interest|"|:|,',"",prors[i])
                    #uid=re.sub(r'borrowerId|"|:|.0|,',"",uids[i])
                    if(len(pid)>0):
                        self.getLender(pid)

                        loanUrl='http://www.we.com/lend/detailPage.action?loanId='+str(pid)
                        loanPage=getloginHTML(loanUrl)
                        loanPage=re.sub("\n","",loanPage)

                        allPat=re.compile(u'<div class="basic-filed "><span>.*?</span><em>(.*?)</em></div>')
                        alls=allPat.findall(loanPage)
                        age=alls[0]
                        edu=alls[1]
                        income=alls[7]

                        house=alls[8]
                        car=alls[10]
                        print age,edu,income,house,car

                        bb=re.compile('"user":[^,]*,')

                        btPat=re.compile('"borrowType":"[^,]*,')
                        blPat=re.compile('"borrowerLevel":"[^,]*,')
                        addPat=re.compile('"address":"[^,]*,')
                        jtPat=re.compile('"jobType":"[^,]*,')
                        nickPat=re.compile('"nickName":"[^,]*,')
                        verifyPat=re.compile('"verifyState":"[^,]*,')
                        marrPat=re.compile('"marriage":"[^,]*,')


                        if(len(loanPage)>0):
                            bbs=bb.findall(loanPage)
                            #print bbs
                            bts=btPat.findall(loanPage)
                            bls=blPat.findall(loanPage)
                            adds=addPat.findall(loanPage)
                            jts=jtPat.findall(loanPage)
                            nicks=nickPat.findall(loanPage)
                            verifys=verifyPat.findall(loanPage)
                            marrs=marrPat.findall(loanPage)

                        #print borids[0]
                            if(len(bbs)>0):
                                bbid=re.sub(r'user|"|:|,',"",bbs[0])
                                print bbid
                                bt=re.sub(r'borrowType|"|:|,',"",bts[0])
                                bl=re.sub(r'borrowerLevel|"|:|,',"",bls[0])
                                add=re.sub(r'address|"|:|,',"",adds[0])
                                jt=re.sub(r'jobType|"|:|,',"",jts[0])
                                nick=re.sub(r'nickName|"|:|,',"",nicks[0])
                                vy=re.sub(r'verifyState|"|:|,',"",verifys[0])
                                ma=re.sub(r'marriage|"|:|,',"",marrs[0])


                        self.getLender(pid)

                        #print ll

                        #print ll
                        self.db.insertProject(pid,pn,pr,ps,pm,bbid,nick,bt)
                        self.db.insertBorrowerInfo(bbid,nick,bl,add,jt,vy,ma,age,edu,income,house,car)
                        #insertBorrowerInfo(self,userid,name,level,address,job,verify,ma,age,edu,income,house,car)

                except:
                    continue


        print "FINISHED: ",page



    #def getBorrower(self,loanId):
        #url='http://www.we.com/lend/detailPage.action?loanId='+str(loanId)
        #loanIndex=getHTML(url)

    def getLender(self,proid):

            lendUrl='http://www.we.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId='+str(proid)
            lendPage=getHTML(lendUrl)
            lendPage=re.sub("\n","",lendPage)
            #print lendPage

            lendidPat=re.compile('"userId":[^,]*,')
            lidPat=re.compile('"id":[^,]*,')

            lendnPat=re.compile('"userNickName":"[^,]*,')
            lendaPat=re.compile('"amount":[^,]*,')
            lendmPat=re.compile('"tradeMethod":"[^,]*,')



            if(len(lendPage)>0):
                lendids=lendidPat.findall(lendPage)
                lids=lidPat.findall(lendPage)
                lendns=lendnPat.findall(lendPage)
                lendas=lendaPat.findall(lendPage)
                lendms=lendmPat.findall(lendPage)
               # ll=""
                #print lendns

                for j in range(0,len(lids)):
                    lendid=re.sub(r'userId|"|:|,',"",lendids[j])
                    lid=re.sub(r'id|"|:|,',"",lids[j])
                    lendn=re.sub(r'userNickName|"|:|}|,',"",lendns[j])
                                #print lendn
                    lenda=re.sub(r'amount|"|:|,',"",lendas[j])
                                #print lenda
                    lendm=re.sub(r'tradeMethod|"|:|,',"",lendms[j])
                   # ll=ll+lendid+"#"+lendn+"#"+lenda+"%"


                    self.db.insertLenderInfo(lendid,lid,proid,lendn,lendm,lenda)





    def setProjectInfo(self,proid,proname,prorate,prostatus,promoney,borrowerId,nickName,borrowerType):

        #self.rruserid=userid
        self.rrproname=proname
        self.rrproid=proid
        self.rrpromoney=promoney
        self.rrprorate=prorate
        self.rrprostatus=prostatus
        self.rrbid=borrowerId
        self.rrnick=nickName
        self.rrbt=borrowerType



    def clearData(self):

        #self.rruserid=""
        self.rrproname=""
        self.rrproid=0
        self.rrpromoney=""
        self.rrprorate=""
        self.rrprostatus=""
        self.rrbid=""
        self.rrnick=""
        self.rrbt=""
        self.rrbl=""
        self.rradd=""
        self.rrjt=""







    def overWrite(self):

        print "proname:",self.rrproname
        print "proid:",self.rrproid
        print "prorate:",self.rrprorate
        print "promoney:",self.rrpromoney
        print "prostatus:",self.rrprostatus
        #print "userid:",self.rruserid



        #self.db.insertProject(self.rrproid,self.rrproname,self.rrprorate,self.rrprostatus,self.rrpromoney,self.rruserid)
        #def insertProject(self,proid,proname,prorate,prostatus,promoney,userid):


if __name__=='__main__':
    url="http://www.we.com/lend/loanList.action"
    html=getHTML(url)
    totalpage=re.compile(r'"totalPage"[^,]*,')
    sumpage=totalpage.findall(html)

    #pageNum = int(re.sub(r'totalPage|"|:|,',"",sumpage[0]))
    a=renrendaiWorker()
    a.db.connectDB("127.0.0.1","root","sinweetyYI316","renrendai")
    a.createTable("127.0.0.1","root","sinweetyYI316","renrendai")

    for y in range(0,2):
        print y
        a.getIndex(y)
    a.db.closeDB()

    print "FINISHED: ",'over'