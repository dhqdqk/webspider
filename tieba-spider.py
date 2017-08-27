#!/usr/bin/env python
#coding: utf-8
import urllib.request
import urllib.error
import urllib.parse
import re
from myspider import Spider


class BaiduSpider(Spider):
    def __init__(self):
        super(BaiduSpider, self).__init__(None, None, "https://baidu.com/", 0)
        self.login_url = 'https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F'


class TiebaSpider(BaiduSpider):
    def __init__(self):
        '''
        lz:发布主题的用户ID
        see_lz：只查看楼主发布的贴子
        baname:贴吧名
        tie_id：主题的ID编号
        rs_tie_title: 匹配贴子页主题的正则表达式
        rs_tie_text: 匹配贴子页内容的正则表达式
        rs_reply_num : 匹配主题总回复数以及总页数
        rs_ba_text: 获取帖吧主题列表（主题回复数量，主题ID，主题）
        rs_titlenums：匹配贴吧主题总数（实际是50倍页面数)
        '''
        super(TiebaSpider, self).__init__()
        self.baseurl = "https://tieba.baidu.com/"
        self.see_lz = '?see_lz=1'
        self.baname = ''
        self.tie_id = ''
        self.rs_tie_title = '<h3 class="core_title_txt.*?title=".*?">(.*?)</h3>'
        self.rs_tie_text = '<div id="post_content_.*?>(.*?)</div>'
        self.rs_reply_num = '<li class="l_reply_num.*?<span.*?>(.*?)</span>.*?<span.*?>(.*?)</span>.*?</li>'
        self.rs_ba_text = '<span class="threadlist_rep_num.*?>(.*?)</span>.*?<a href="/p/(.*?)" title=.*?">(.*?)</a>'
        self.rs_titlenums = '<a href=".*?pn=(.*?)" class="last.*?">.*?</a>'
        self.floor = 1

    def get_ba(self, baname, page_point=0):
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

    def get_titles(self, page):
        '获取贴吧页面的主题列表（主题回复数量，主题ID，主题）'
        pattern = re.compile(self.rs_ba_text, re.S)
        res = re.findall(pattern, page)
        return res

    def get_titlenums(self, page):
        '获取贴吧主题尾页主题总数'
        pattern = re.compile(self.rs_titlenums)
        res = re.search(pattern, page)
        return int(res)

    def get_page(self, tie_id, page_index=1, see_lz=False):
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

    def get_title(self, page):
        pattern = re.compile(self.rs_tie_title)
        res = re.search(pattern, page)
        if res:
            return res.group(1).strip()
        else:
            return None

    def get_reply_num(self, page):
        '获取主题回复数及总页数，返回元组（回复数，页数）'
        pattern = re.compile(self.rs_reply_num)
        res = re.search(pattern, page)
        if res:
            return res.groups()
        else:
            return None

    def get_tie_text(self, page):
        '抓取页面的贴子内容'
        pattern = re.compile(self.rs_tie_text, re.S)
        items = re.findall(pattern, page)
        content = []
        for i in items:
            content.append(self.tool.replace(i))
        return content

    def searchba(self,baname, user, debug=None):
        url = "http://tieba.baidu.com/f/search/res?ie=utf-8"
        data = urllib.parse.urlencode({"kw1":baname, "tb":user}).encode("gbk")
        req = urllib.request.Request(url, data, headers=self.headers)
        res = urllib.request.urlopen(req)
        return res.read().decode("gbk")


    def searchall(self, user):
        url = "http://tieba.baidu.com/f/search/res?ie=utf-8&qw="
        data = urllib.parse.urlencode({"kw1": "", "tb": user}).encode("utf-8")
        req = urllib.request.Request(url, data, headers=self.headers)
        res = urllib.request.urlopen(req)
        return res.read().decode("gbk")


if __name__ == "__main__":
    b = TiebaSpider()
    print(b.baseurl)
    print(b.searchba("健美", "炫彩703"))
    print(b.searchall("炫彩703"))