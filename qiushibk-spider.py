#!/usr/bin/env python3
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

'''
.*?组合匹配任意字符不限次数。
(.*?)为分组，默认从0开始。
re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。
'''

class QSBK(Spider):
    def __init__(self):
        '''
        糗事百科段子爬虫；
        rs:段子的html代码匹配式；
        enbale：段子交互浏览开闭标记
        page_content：抓取的段子存放列表
        '''
        super(QSBK, self).__init__(sqlit=None, cur=None, baseurl="http://www.qiushibaike.com/hot/page/", total=0)
        self.rs = '<div class="author clearfix">.*?<a.*?<h2>(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?<i.*?number">(.*?)</i>.*?<a.*?<i.*?number">(.*?)</i>'
        self.pattern = re.compile(self.rs, re.S)
        self.enble = False
        self.page_content = []

    def get_page(self, page_index):
        '连接单个页面并获取html代码'
        try:
            url = self.baseurl + str(page_index)
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            if hasattr(e, 'reason'):
                print(u'连接糗事百科失败，原因：', e.code, e.reason)
                return None
        page_code = response.read().decode('utf-8')
        return page_code

    def get_items(self, page_index):
        '提取页面中的内容;去掉带图片的条目'
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

    def load_page(self):
        '当内容盒中条目少于2个时，加载并抓取新的一页'
        if self.enble == True:
            if len(self.page_content) < 2:
                content = self.get_items(self.page_index)
                if content:
                    self.page_content.append(content)
                    self.page_index += 1

    def read_item(self, page_content, page_index):
        '用户端，按键逐条显示条目'
        for story in page_content:
            order = input()
            self.load_page()
            if order in 'Qq':
                self.enble = False
                return
            print()
            print("第%d页\t发布人%s\t%s笑评\t%s条评论\n%s" % (page_index, story[0], story[2], story[3], story[1]))

    def start(self):
        '启动互动界面'
        print("糗事百科段子爬虫；按任意键显示下一页内容；按Q/q/enter回车键则退出：")
        self.enble = True
        self.load_page()
        nowpage = 0
        while self.enble:
            if len(self.page_content) > 0:
                r = self.page_content[0]
                del self.page_content[0]
                nowpage += 1
                self.read_item(r, nowpage)


if __name__ == "__main__":
    t = QSBK()
    t.start()
