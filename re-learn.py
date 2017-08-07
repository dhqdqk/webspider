#!/usr/bin/env python
#coding:utf-8

import re

#re.match()
m = re.match(r'(\w+) (\w+)(.*)', 'hello world!')

print("m.string", m.string)
print("m.re:", m.re)
print("m.pos:", m.pos)
print("m.endpos:", m.endpos)
print("m.lastindex:", m.lastindex)
print("m.lastgroup:", m.lastgroup)
print("m.group():", m.group())
print("m.group(1,2,3):", m.group(1, 2, 3))
print("m.groups():", m.groups())
print("m.groupdict():", m.groupdict())
print("m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3'))

#re.search()
p = re.compile(r'world')
se = re.search(p, 'hello world!')
if se:
    print("se.group():", se.group())

#re.split()
p = re.compile(r'\d+')
sp = re.split(p, 'one1two2three3four4')
if sp:
    print("split():", sp)

#re.findall()
p = re.compile(r'\d+')
fa = re.findall(p, 'one1three3two2')
if fa:
    print("findall():", fa)


#re.finditer()
fi = re.finditer(p, 'one1two2three3')
for i in fi:
    print("finditer:", i.group())
