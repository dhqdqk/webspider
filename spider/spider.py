#!/usr/bin/env python
#coding:utf-8

import urllib
import re
import os
import sqlite3
import cookielib
import time

def new_headers(user_agent='', referer=None):
    if referer:
        return {'User-Agent': user_agent; 'Referer': referer}
    return {'User-Agent': user_agent}

class Spider(object):
    def __init__(self, sqlit=None, cur=None, baseurl='', total=0):
        self.sqlite = sqlit
        self.cur = cur
        self.baseurl = baseurl
        self.total = total
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'}
        self.timeout = 10

    def qutoSin(self, string):
        return string.replace("'", "")


    def login(self, login_url):
        pass

    def created_db(self, db):
        pass

    def parse(self, url, debug=False):
        pass


class SpiderBaidu(Spider):
    "baidu spider"
    def __init__(self):
        super(SpiderBaidu, self).__init__(sqlit=None, cur=None, baseurl="http://www.baidu.com", total=0)

    def login(self, user, pwd, login_url='https://passport.baidu.com/v2/?login'):
        cookie = cookielib.CookieJar()
        cookieProc = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(cookieProc)
        urllib.request.install_opener(opener)

        post = {
                'username': user,
                'password': pwd,
                'tpl': 'mn',
                'u': "http://www.baidu.com/",
                'psp_tt': 0,
                'mem_pass': 'on'
                }
        post = urllib.urlencode(post)

        req = urllib.request.Request(
                              url=login_url,
                              data=post,
                              headers=self.header,
                              timeout=self.timeout
                              )
        res = urllib.request.urlopen(req).read(500)

        if 'passCookie' in res:
            flag = True
        else:
            flag = 'login fail:%s' % user

        return flag

    def created_db(self, dbFile):
        dbFile = dbFile.replace("\\","/")
        self.sqlit = sqlite3.connect(dbFile)
        self.cur = self.sqlit.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS `article`
            (
                 a_id char(24) PRIMARY KEY,
                 title varchar(255),
                 created_time datetime,
                 category varchar(255),
                 orgurl varchar(255),
                 content text
            )
            """
        self.cur.execute(sql)
        self.sqlit.commit()

    def parse_html(self,url,debug=False):

        '''
            分析页面
            url 为要分析页面的起始URL
            debug 当为True时，将会打印出调试信息
        '''
        while True:
            c = urllib.request.urlopen(url).read()

            #标题，时间
            #正则编义(注意后面的修饰)
            p = re.compile(
                    r'<div.*?id="?m_blog"?.*?<div.*?class="?tit"?>(.*?)<\/div>.*?<div.*?class="?date"?>(.*?)<\/div>',
                    re.S|re.I
                    )
            m = p.search(c)
            if m==None:
                break
            title = m.group(1).strip()
            date  = m.group(2).strip()
            date  = date.split(' ')
            date  = date[0]+' '+date[1]

            #内容
            s = re.compile(
                    r'<div\s*?id="?blog_text"?\s*?class="?cnt"?\s*?>(.*?)<\/div>',
                    re.S|re.I
                )
            m = s.search(c)
            content = m.group(1).strip()

            #类别
            s = re.compile(
                    '类别：(.*?)<\/a>',
                    re.S|re.I|re.U
                )
            m = s.search(c)
            category = m.group(1).strip()

            #源链接
            orgurl = re.compile(
                    'myref.*?=.*?encodeURIComponent\("(.*?)"\)',
                    re.S|re.I|re.U
                )
            orgurl = orgurl.search(c)
            orgurl = orgurl.group(1).strip()
            aid = os.path.split(orgurl)
            aid = aid[1].split('%2E')[0]

            #通过元组
            sql = 'insert into `article`(a_id,title,created_time,category,orgurl,content)'
            values = "values('%s','%s','%s','%s','%s','%s')"%(aid,self.qutoSin(title),
                    date,self.qutoSin(category),orgurl,self.qutoSin(content))
            sql+=values

            #插入数据库
            self.cur.execute(sql)
            self.sqlit.commit()
            self.total +=1

            #下一篇
            nexturl = re.compile(
                    'var\s*?post\s*?=\s*?\[true,\'.*?\',\'.*?\',(.*?)]',#注意这里最后一个]没手动加转义符\
                     re.S|re.I|re.U
                )
            nexturl = nexturl.search(c)
            if nexturl==None:
                break
            nexturl = self.qutoSin(nexturl.group(1).strip()).replace("\\",'')
            nexturl = self.baseurl+nexturl
            url = nexturl
            #输出调试信息
            if debug:
                print(title)
                print(date)
                print('nextUrl:'+url+'\n')

            time.sleep(1)
