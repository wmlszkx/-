# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 02:42:26 2021

@author: 邹可馨
"""

import urllib.request
import re
 
url = "https://movie.douban.com/top250"#之前单引号有bug，要改为双引号
request = urllib.request.Request(url)
request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
response = urllib.request.urlopen(request)
buf = response.read()
buf = str(buf, encoding='utf-8')
# print(buf)
# 获取所有图片url地址列表
listurl = re.findall(r'http.+\.jpg', buf)
print(listurl)
 
i = 1
for url in listurl:
    f = open(str(i)+'.jpg', 'wb+')
    req = urllib.request.urlopen(url)
    buf = req.read()
    # buf = str(buf)
    f.write(buf)
    i += 1
    if i>20:#取20张
        break
