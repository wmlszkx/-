# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 02:38:01 2021

@author: 邹可馨
"""

import requests
import os
url = "https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/bd_logo1_31bdc765.png"
root = "D://python学习//爬虫//照片//"
path = root + url.split("/")[-1]
try:
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url)
        r.raise_for_status()
        #使用with语句可以不用自己手动关闭已经打开的文件流
        with open(path,"wb") as f: #开始写文件，wb代表写二进制文件
            f.write(r.content)
        print("爬取完成")
    else:
        print("文件已存在")
except Exception as e:
    print("爬取失败:"+str(e))
