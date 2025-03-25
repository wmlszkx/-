# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 02:28:53 2021

@author: 邹可馨
"""
import requests
#正则  参考https://docs.python.org/zh-cn/3/library/re.html
import re
#操作 https://docs.python.org/zh-cn/3/library/os.html?highlight=os#module-os
import os

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
name = input('您要爬取什么图片')
num = 0
x = input('您要爬取几张呢?，输入1等于20张图片。')
for i in range(int(x)):
    # 下载到本地图片的位置
    name_1 = 'D:\\python学习\\'
    # 根据百度图片url发现可以将输入的种类拼接得到对应图片集
    url = 'https://weibo.com/mayday?tabtype=album&uid=3365597502&index=7'
    res = requests.get(url,headers=headers)
    print(res)
    htlm_1 = res.content.decode()
    # 正则匹配解析后的html  注意：这里也可以用python解析html的BeautifulSoup4工具或者pyquery等进行匹配
    a =re.findall('<img scr="(.*?)"',htlm_1)
    # 如果没有文件夹就创建
    if not os.path.exists(name_1):
        os.makedirs(name_1)
    # 循环写到本地
    for b in a:
        num = num +1
        try:
            img = requests.get(b)
   

        except Exception as e:
                    print('第'+str(num)+'张图片无法下载------------')
                    print(str(e))
                    continue
        f = open(name_1+name+str(num)+'.jpg','ab')
        print('---------正在下载第'+str(num)+'张图片----------')
        f.write(img.content)
        f.close()
print('下载完成')

