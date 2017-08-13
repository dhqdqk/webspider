#!/usr/bin/env python
#coding: utf-8
import urllib.request
import urllib.error
import re
from spider.spider import Spider

class TiebaSpider(Spider):
    def __init__(self):
        '''
        lz:发布主题的用户ID
        see_lz：只查看楼主发布的贴子
        baname:贴吧名
        tie_id：主题的ID编号
        rs_tie_title: 匹配贴子页主题的正则表达式
        rs_tie_text: 匹配贴子页内容的正则表达式
        rs_reply_num : 匹配主题总回复数以及总页数
        '''
        super(TiebaSpider, self).__init__(None, None, "http://tieba.baidu.com/", 0)
        self.see_lz = '?see_lz=1'
        self.baname = ''
        self.tie_id = ''
        self.rs_tie_title = '<h3 class="core_title_txt.*?title=".*?">(.*?)</h3>'
        self.rs_tie_text = ''
        self.rs_reply_num = '<li class="l_reply_num.*?<span.*?>(.*?)</span>.*?<span.*?>(.*?)</span>.*?</li>'
        # '<div class="l_post.*?<a class="p_author.*?>(.*?)</a>.*?<div id="post_content_.*?>(.*?)</div>'
        self.rs_tie_text = '<div id="post_content_.*?>(.*?)</div>'
        self.floor = 1

    def get_page(self, tie_id, page_index, see_lz=False):
        '获取单个主题的html页面；主题页面数从1开始，按1递增。'
        if see_lz:
            url = self.baseurl + 'p/' + str(tie_id) + self.see_lz + '&pn=' + str(page_index)
        else:
            url = self.baseurl + 'p/' + str(tie_id) + '&pn=' + str(page_index)
        try:
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            if hasattr(e, "reason"):
                print("连接百度贴吧失败：", e.code, e.reason)
            return None
        return response.read().decode('utf-8')

    def get_ba(self, baname, page_point):
        '获取贴吧的主题清单；page_point按断点方式取值，从0开始，按50递增（下个断点为50）；'
        url = self.baseurl + 'f?kw=' + baname + '&ie=utf-8&pn=' + str(page_point)
        try:
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            if hasattr(e, "reason"):
                print("连接贴吧主题页面失败：", e.code, e.reason)
                return None
        return response.read().decode('utf-8')

    def get_title(self, page):
        pattern = re.compile(self.rs_tie_title)
        res = re.search(pattern, page)
        if res:
            return res.group(1).strip()
        else:
            return None

    def get_reply_num(self, page):
        '获取主题回复数及总页数，返回二组（回复数，页数）'
        pattern = re.compile(self.rs_reply_num)
        res = re.search(pattern, page)
        if res:
            return res.groups()
        else:
            return None

    def get_tie_text(self, page):
        pattern = re.compile(self.rs_tie_text, re.S)
        items = re.findall(pattern, page)
        content = []
        for i in items:
            content.append(self.tool.replace(i))
        return content


if __name__ == "__main__":
    b = TiebaSpider()
    print(b.baseurl)
    #print(b.get_ba('ubuntu', 0))
    b.tie_id = 3138733512
    p = b.get_page(b.tie_id, 1, True)
    t = b.get_reply_num(p)
    print(t)
    for i in b.get_tie_text(p):
        print(i)
        print(b.floor, '楼', '-' *30, '\n')
        b.floor += 1
