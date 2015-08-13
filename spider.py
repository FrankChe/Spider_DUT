# -*- coding: utf-8 -*- 


__author__ = 'chexiaoyu'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import cookielib
import re
from pyquery import PyQuery as pq
import getpass
#DUT计算绩点

#项目存在的问题：由于大连理工大学教务处的网站的成绩查看页面是JS产生的，Url中最后一个参数是通过js动态产生的，目前不是到应该如何解决该问题。

class DUT:

    def __init__(self,username,password):
        #登陆Url
        self.loginUrl = 'http://202.118.65.21:8089/loginAction.do'
        #本学期成绩Url
        #self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fa'
        self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4242'
        #self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=001'
        #self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fa:164'
        self.cookies = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'zjh':username,
            'mm':password
        })
        #构建opener
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        #学分list
        self.credit = []
        self.grades = []



    #获取本学期成绩页面
    def getPage(self):
        request = urllib2.Request(
            url = self.loginUrl,
            data = self.postdata)
        result = self.opener.open(request)
        result = self.opener.open(self.gradeUrl)
        
        #print result.read().decode('gbk')
        #打印登陆内容

        return result.read().decode('gbk')
        #return result.read()

    def get_trueUrl(self):
        page = self.getPage()


    def getGrades(self):
        #获得本学期成绩页面
        page = self.getPage()

        #print page

        d = pq(page)
        #print d
        p = d('.odd')
        #print p
        #print pq(p).find('tr td td td')
        #for i in range(len(p)):
        #     temp = p.pq(i).find('td').eq(2).text()
        #     print temp
        for i in p:
            self.credit.append(float(pq(i).find('td').eq(4).text()))
            self.grades.append(float(pq(i).find('td p').eq(0).text().encode("utf-8")))




        # for i in range(len(self.credit)):
        #     self.credit[i] = map(float,self.credit[i])
        #     self.grades[i] = map(float,self.grades[i])
        # self.credit = map(float,self.credit)
        # self.grades = map(float,self.grades)
        # self.credit = [float(i) for i in self.credit]
        # self.grades = [float(i) for i in self.grades]

        #print self.credit
        #print self.grades



             #self.grades.extend(pq(i).text())
             #print self.grades

        #正则匹配
        #print page

        # myItems = re.findall('<tr\sclass[\s\S]*?<td[\s\S]*?<td[\s\S]*?<td[\s\S]*?>([\s\S]*?)</td>[\s\S]*?<p[\s\S]*?>(.*?)&',page,re.S)
        #
        # #print myItems
        # for item in myItems:
        #     print item
        #     self.credit.append(item[0].encode('gbk'))
        #     self.grades.append(item[1].encode('gbk'))
        #     print item
        # self.getGrade()

    # def getGrade(self):
    #     #计算总绩点
    #     sum = 0.0
    #     weight = 0.0
    #     for i in range(len(self.credit)):
    #         if(self.grades[i].isdigit()):
    #             sum += string.atof(self.credit[i])*string.atof(self.grades[i])
    #             weight += string.atof(self.credit[i])
    #
    #     print u"绩点为：",sum/weight

    def getGrade(self):
        #计算总绩点
        self.getGrades()
        sum = 0.0
        weight = 0.0
        for i in range(len(self.credit)):
            sum += self.credit[i] * self.grades[i]
            weight += self.credit[i]
        print "你的平均成绩为：",sum/weight
        print "你的GPA为（标准算法）:",sum*4/(weight*100)





print "请输入学号和密码："
username = raw_input()
password = getpass.getpass()

# username = '201292100'
# password = '310014'
dut = DUT(username,password)
dut.getGrade()
#dut.getPage()