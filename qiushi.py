#!/usr/bin/env python
#coding: utf-8

import urllib
import urllib.request
import urllib.error
import re
from spider.spider import Spider

'''
实践内容：
1.抓取糗事百科的段子
2.过滤带有图片的段子
3.实现每按一次回车显示一个段子的发布时间，发布人，段子内容，点赞数。
'''

page_index = 1
url = "http://www.qiushibaike.com/hot/page/" + str(page_index)
user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'
headers = { 'User-Agent' : user_agent }

try:
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
except urllib.error.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)

'''
.*?组合匹配任意字符不限次数。
(.*?)为分组，默认从0开始。
re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。
'''
pattern = re.compile('<div class="author clearfix">.*?<a.*?<h2>(.*?)</h2>.*?'+
        '<div.*?content">.*?<span>(.*?)</span>.*?<i.*?number">(.*?)</i>.*?<a.*?<i.*?number">(.*?)</i>',
                    re.S)
items = re.findall(pattern, content)
print(len(items))
for item in items:
    print("-" * 20)
    # item[1]表示文章内容，内容中可能带有图片，过滤掉
    have_img = re.search('img', item[1])
    if have_img:
        pass
    print(item[0], item[1], item[2], item[3])

class QSBK(Spider):
    def __init__(self):
        super(QSBK, self).__init__(sqlit=None, cur=None, baseurl="http://www.qiushibaike.com/hot/page/", total=0)
        self.rs = '<div class="author clearfix">.*?<a.*?<h2>(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?<i.*?number">(.*?)</i>.*?<a.*?<i.*?number">(.*?)</i>'
        self.pattern = re.compile(self.rs, re.S)
        self.enble = False
        self.stories = []

    def get_page(self, page_index):
        try:
            url = self.baseurl + str(page_index)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            page_code = response.read().decode('utf-8')
            return page_code
        except urllib.error.HTTPError as e:
            if hasattr(e, 'reason'):
                print(u'连接糗事百科失败，原因：', e.code, e.reason)
                return None

    def get_items(self, page_index):
        page_code = self.get_page(page_index)
        if not page_code:
            print(u'页面加载失败……')
            return None
        items = re.findall(self.pattern, page_code)
        page_content = []
        for item in items:
            have_img = re.search('img', item[1])
            if have_img:
                pass
            del_br = re.compile('<br/>')
            text = re.sub(del_br, "\n", item[1]).strip()
            page_content.append([item[0].strip(), text, item[2].strip(), item[3].strip()])
        return page_content

    def load_page(self, page):
        if self.enble == True:
            if len(self.stories) < 2:
                page_content = self.get_items(self.page_index=)
                if page_content:
                    self.stories.append(page_content)
                    self.page_index += 1
