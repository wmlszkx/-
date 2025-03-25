# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 01:24:58 2021

@author: 邹可馨
"""
import urllib.parse
import json
import jsonpath
import requests

url='https://weibo.com/mayday?tabtype=album&uid=3365597502&index=7'
we_data=requests.get(url).text
html=json.loads(we_data)
photo=jsonpath.jsonpath(html,'$..img src')#不管前面多少，找到该值对应链接
print(photo)