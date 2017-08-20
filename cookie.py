#!/usr/bin/env python
#coding:utf-8

import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar

'''
http.cookiejar模块的主要作用是提供可存储cookie的对象，以便于与urllib2模块配合使用来访问Internet资源。
http.cookiejar模块非常强大，我们可以利用本模块的CookieJar类的对象来捕获cookie并在后续连接请求时重新发送，
比如可以实现模拟登录功能。该模块主要的对象有CookieJar、FileCookieJar、MozillaCookieJar、LWPCookieJar。

它们的关系：CookieJar —-派生—->FileCookieJar  —-派生—–>MozillaCookieJar和LWPCookieJar

MozillaCookieJar可将cookie信息保存到文本

in Python2:

import cookielib

in Python3:

import http.cookiejar
'''

# 创建cookieJar实例对象
cookie = http.cookiejar.CookieJar()
# 构建cookie处理器
handler = urllib.request.HTTPCookieProcessor(cookie)
# 构建可处理cookie的url处理器opener
opener = urllib.request.build_opener(handler)

url = 'http://www.baidu.com'
res = opener.open(url)
# 检查接收的cookie信息
for item in cookie:
    print('name = ' + item.name)
    print('Value = ' + item.value)

# cookie保存到文本
filename = 'cookie.txt'
cookie2 = http.cookiejar.MozillaCookieJar(filename)
handler2 = urllib.request.HTTPCookieProcessor(cookie2)
opener2 = urllib.request.build_opener(handler2)
res2 = opener2.open(url)
cookie2.save(ignore_discard=True, ignore_expires=True)
'''
ignore_discard的意思是即使cookies将被丢弃也将它保存下来，
ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
'''

# cookie读取
cookie3 = http.cookiejar.MozillaCookieJar()
cookie3.load(filename, ignore_discard=True, ignore_expires=True)
opener3 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie3))
req = urllib.request.Request(url)
res = opener3.open(req)
print(res.read(100).decode('utf-8'))

# cookie登录百度
baidu_cookie = 'baidu_cookie.txt'
login_url = 'https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F'
cookie = http.cookiejar.MozillaCookieJar(baidu_cookie)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
# 将用户名和密码打包成字节码
postdata = urllib.parse.urlencode({
            'userName': "dhqdqk",
            'password': "dhq96dqkbd.."
}).encode(encoding='UTF8')
res = opener.open(login_url, postdata)
cookie.save(ignore_discard=True, ignore_expires=True)
tieba_url = 'https://tieba.baidu.com/index.html'
res = opener.open(tieba_url)
print(res.read().decode('utf-8'))
