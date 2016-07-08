#!/usr/bin/env python
#coding:utf-8

import urllib
import urllib2

#Request(url, data, headers)
request = urllib2.Request("http://www.baidu.com")

#urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT)
#response = urllib2.urlopen("http://www.baidu.com")
response = urllib2.urlopen(request)
print response.read()
print '-' * 20

'''
#request with POST 
values = {"username":"dhqdqk", "password":""}
data = urllib.urlencode(values)
url = "https://passport.baidu.com/v2/?login"
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
print response.read()
'''

#POST 
values = {}
values['username'] = "dhqdqk"
values['password'] = ''
data = urllib.urlencode(values)
url = "https://passport.baidu.com/v2/?login"
geturl = url + "?" + data
print "geturl:\n", geturl
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()