#!/usr/bin/env python3
#coding:utf-8

import urllib
import urllib.request
import urllib.parse
import urllib.error
import re
import os
import sqlite3
import http.cookiejar
import _thread
import time

def new_headers(user_agent=None, referer=None):
    if not user_agent:
        user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
    if referer:
        return {'User-Agent': user_agent, 'Referer': referer}
    return {'User-Agent': user_agent}


class AddCookies(object):
    '''
    在HTTP请求中加入COOKIES；

    '''
    def __init__(self):
        pass

    def new_cookie(self, file=""):
        '首次访问，获取新的COOKIES；生成self.opener对象'
        if file:
            self.cookies = http.cookiejar.MozillaCookieJar(self.file)
        else:
            self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))

    def load(self, file=""):
        '已存有COOKIES，直接加载COOKIES文件'
        if file:
            self.cookies = http.cookiejar.MozillaCookieJar()
            self.cookies.load(file, ignore_discard=True, ignore_expires=True)

    def save(self):
        '保存当前的COOKIES于指定文件'
        self.cookies.save(ingore_discard=True, ignore_expires=True)

class DelHTMLTag(object):
    ''''
    去除文本中的html标记和代码,img标签，超链接；
    替换换行标签为\n，TD标签为\t，p标签为\n加两空格，br标签改为\n；
    '''
    rmImg = re.compile('<img.*?>| {7}|')
    rmAddr = re.compile('<a.*?>|</a>')
    rpLine = re.compile('<tr>|<div>|</div>|</p>')
    rpTD = re.compile('<td>')
    rpPara = re.compile('<p.*?>')
    rpBr = re.compile('<br><br>|<br>')
    rmScript = re.compile('<script>.*?</script>')
    rmExtra = re.compile('<.*?>')
    rmBlank = re.compile('\b*')
    rmBLine = re.compile('\n[\s| ]*\r')

    def replace(self, x):
        x = re.sub(self.rmImg, "", x)
        x = re.sub(self.rmAddr, "", x)
        x = re.sub(self.rpLine, "\n", x)
        x = re.sub(self.rpTD, "\t", x)
        x = re.sub(self.rpPara, "\n  ", x)
        x = re.sub(self.rpBr, "\n", x)
        # x = re.sub(self.rmScript, '', x)
        x = re.sub(self.rmExtra, "", x)
        return x.strip()


class Spider(object):
    def __init__(self, sqlit=None, cur=None, baseurl='', total=0):
        '''
        sqlit：是否指定sqlit存储数据（如cookie）；
        cur：存储数据文件的目录
        baseurl:指定抓爬的目标URL
        referer:如果主机站点要求验证请求合法性，则要加上
        pattern:提取网页内容时的正则匹配式，不同网站通常不同。
        login_url：站点的登录页面
        tool: DdelHTMLTag的实例，调用方法replace()用于去除html标记
        '''
        self.sqlite = sqlit
        self.cur = cur
        self.baseurl = baseurl
        self.total = total
        self.user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'
        self.referer = None
        self.headers = new_headers(self.user_agent, self.referer)
        self.timeout = 10
        self.page_index = 1
        self.pattern = ''
        self.login_url = ''
        self.tool = DelHTMLTag()

    def qutoSin(self, string):
        return string.replace("'", "")

    def login(self, postdata, cookie_file=''):
        '''
        站点设定不允许非登录请求或限制资源获取的范围时，要通过cookie登录
        '''
        pass

    def created_db(self, db):
        pass

    def get_page(self, page_index, debug=False):
        '连接单个页面并获取html代码'
        pass

    def get_pages(self, page_index, debug=False):
        '''
        批量抓取网页内容
        '''
        pass

    def get_items(self, page_index):
        '提取网页内容'
        pass


class SpiderBaidu(Spider):
    "baidu spider"
    def __init__(self):
        super(SpiderBaidu, self).__init__(sqlit=None, cur=None, baseurl="http://www.baidu.com", total=0)
        self.login_url = 'https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F'

    def login(self, user, pwd, login_url):
        cookie = http.cookielib.CookieJar()
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

    def get_pages(self,url,debug=False):

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
