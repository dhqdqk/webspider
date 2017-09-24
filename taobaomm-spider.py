#!/usr/bin/env python3
#coding: utf-8

import urllib.request
import urllib.error
import re
import os
from myspider import Spider

class TaobaommSpider(Spider):
    '''
    抓取淘宝美眉的信息和图片
    '''
    def __init__(self):
        super(TaobaommSpider, self).__init__()
        self.baseurl = "https://mm.taobao.com/json/request_top_list.htm?page="

    def get_page(self, page_index):
        '抓取淘宝美眉索引页HTML'
        url = self.baseurl + str(page_index)
        req = urllib.request.Request(url, headers=self.headers)
        res = urllib.request.urlopen(req)
        return res.read().decode('gbk')

    def get_items(self, page):
        'return the users tuple data(icon-imag-url, user-id, user-name, age, location)'
        rs = '<div class="pic-word.*?<a href=.*?<img src="(.*?)".*?<a class="lady-name.*?user_id=(.*?)".*?">(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
        pattern = re.compile(rs, re.S)
        res = re.findall(pattern, page)
        return res

    def get_userpage(self, id):
        '抓取用户主页的HTML'
        url = "https://mm.taobao.com/self/model_info.htm?user_id=%s&is_coment=false" % id
        req = urllib.request.Request(url, headers=self.headers)
        res = urllib.request.urlopen(req)
        return res.read().decode('gbk')

    def create_dir(self, items, pdir="taobaomm"):
        'work-dir/taobaomm;在目录taobaomm下给美眉创建个人目录'
        if pdir == 'taobaomm':
            pdir = os.path.abspath(os.path.dirname(__file__)) + os.sep + pdir
        if not os.path.exists(pdir):
            os.makedirs(pdir)
        for i in items:
            dir = pdir + os.sep + i[2]
            if not os.path.exists(dir):
                os.mkdir(dir)

    def userdir(self, username, pdir="taobaomm"):
        if pdir == 'taobaomm':
            pdir = os.path.abspath(os.path.dirname(__file__)) + os.sep + pdir
        dir = pdir + os.sep + username
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def get_userinfo(self, page):
        rs = ''
        pass

    def get_albums(self, id):
        url = "https://mm.taobao.com/self/model_album.htm?user_id=%s" % id
        req = urllib.request.Request(url, headers=self.headers)
        res = urllib.request.urlopen(req)
        page = res.read().decode('gbk')
        print(page)
        rs = '<h4.*?<a href="(.*?)"'
        pattern = re.compile(rs)
        res = re.search(pattern, page)
        return res


if __name__ == "__main__":
    t = TaobaommSpider()
    text = t.get_page(1)
    i = t.get_items(text)
    t.create_dir(i)
    pp = t.get_userpage(i[0][1])
    a = t.get_albums(i[0][1])
