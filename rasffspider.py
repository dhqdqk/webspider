#!/usr/bin/env python
# coding:utf-8

import urllib.request
import urllib.error
import re
import os

from myspider import Spider
class RasffSpider(Spider):
	def __init__(self):
		super(RasffSpider, self).__init__()
		self.baseurl = "http://db.foodmate.net/rasff/"
		self.tag = "转基因"
		self.code = 'gb2312'
		self.charset = '<head.*?<meta.*?charset=(.*?)">'
		self.rs = r'<tr bgcolor="#f4.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)\r\n</td>.*?<td.*?>.*?href="(.*?)".*?</td>.*?</tr>'

	def newurl(self, page_num):
		url = self.baseurl + "list_" + str(page_num) + ".html"
		return url

	def test(self, num):
		self.pattern = self.newpattern(self.rs)
		self.url = self.newurl(num)
		page = self.get_page(self.url)
		print(page)

def check_gmo(file):
	f = open(file, 'r')
	fact = ["米", "麦", "面", "玉米"]
	d = {i:0 for i in fact}
	print(d)
	for line in f.readlines():
		for i in fact:
			if i in line:
				d[i] += 1
				continue
	f.close()
	return d
if __name__ == "__main__":
	r = RasffSpider()
	r.total = 280
	r.filename = "rasff.txt"
	# r.test(150)
	'''
	file = open(r.filename, 'w+')
	title = "编号" + "\t" + "通报国" + "\t" + "通报产品/来源地" + "\t" + "通报原因" + "\t" + "通报日期" + "\n"
	file.write(title)
	file.close()

	r.pattern = r.newpattern(r.rs)
	r.opattern = r.newpattern(r.charset, tag=True)
	for num in range(1, 281):
		r.url = r.newurl(num)
		print(r.url)
		page = r.get_page(r.url)
		items = r.get_items(page)
		if not items:
			continue
		for i in items:
			if r.tag in i[3]:
				# u = '<a href="'+ r.baseurl +  i[5] + '">查看详情</a>'
				s = i[0] + "\t" + i[1] + "\t" + i[2] + "\t" + i[3] + "\t" + i[4] + "\n"
				print(s)
				with open(r.filename, 'a+') as f:
					f.write(s)

	'''
	d = check_gmo(r.filename)
	for i in d:
		print(i,">>>", d[i])