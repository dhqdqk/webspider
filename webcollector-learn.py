#!/usr/bin/env python
#coding:utf-8

import urllib
import urllib.error
import urllib.request
from urllib.request import urlopen
# The urllib2 module has been split across several modules in Python 3.0 named urllib.request and urllib.error.

#Request(url, data, headers)
request = "http://www.baidu.com"

#urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT)
#response = urllib.request.urlopen("http://www.baidu.com")
'''
This function always returns an object which can work as a context manager and has methods such as

geturl() — return the URL of the resource retrieved, commonly used to determine
    if a redirect was followed
info() — return the meta-information of the page, such as headers, in the form
    of an email.message_from_string() instance (see Quick Reference to HTTP Headers)
getcode() – return the HTTP status code of the response.
'''
response = urlopen(request)
print("geturl():", response.geturl())
print("info()", response.info())
print("getcode()", response.getcode())
print(response.read(100).decode('utf-8'))
print('-' * 20)

'''
#request with POST
'''

#POST
values = {}
values['username'] = "dhqdqk"
values['password'] = ''
data = urllib.parse.urlencode(values)
#the resultant string is to be used as a data for POST operation with the urlopen() function
url = "https://passport.baidu.com/v2/?login"
geturl = url + "?" + data
print("geturl:\n", geturl)
request = urllib.request.Request(geturl)
# urllib.request.Request()是唯一可改变请求方式的方法
response = urllib.request.urlopen(request)
print(response.read(150))

#urllib.error
'''
urllib.error.URLError规定本机访问远程主机的过程中的问题处理方式。
urllib.error.HTTPError是URLError的子类，规定主机反馈的信息存在的问题的处理方式；
3开头的代号可以被处理，100-299范围的号码指示请求成功，400-599代码表示请求遇到错误。
'''
req = 'http://google.com/'
try:
    res = urllib.request.urlopen(req)
    print("work")
    print(res.read(150).decode('utf-8'))
except urllib.error.URLError as e:
    print("error work")
    print(e.reason)

req = 'http://blog.csdn.net/dhqdqk'
try:
    res = urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(e.code, e.reason)
