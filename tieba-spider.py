#!/usr/bin/env python
#coding: utf-8
import urllib.request
import urllib.error
import re
from spider.spider import Spider

class TiebaSpider(Spider):
    def __init__(self):
        super(TiebaSpider, self).__init__(None, None, "http://tieba.baidu.com/", 0)


if __name__ == "__main__":
    b = TiebaSpider()
    print(b.baseurl)
