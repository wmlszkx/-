# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 21:41:30 2021

@author: 邹可馨
"""

from bs4 import BeautifulSoup
import os
import time

from flask import request_finished
#

# 使用requests的get方法获取图片资源

class BeautifulPicture:
    def __init__(self):
        # 使用header用来模拟浏览器
        # 为了应对浏览器的反爬机制（不接受来自代码的访问），使用浏览器的headers来进行伪装
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        self.web_url = 'https://weibo.com/mayday?tabtype=album'
        # 保存图片的文件夹路径
        self.folder_path = 'D:\python'

	#对requsets库的get方法进行封装
    def request(self, url):
        r = request_finished.get(url, headers=self.headers, timeout=100)
        return r
	
    def mkdir(self, path):
        path = path.strip()
        if not os.path.exists(path):
            print("创建名字为", path, "的文件夹")
            os.makedirs(path)
            print("创建成功！")
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def save_img(self, url, name):
        print("开始保存图片……")
        img = self.request(url)
        time.sleep(5)
        file_name = name + '.jpg'
         # 不是新的文件夹且该文件在文件夹中，则不需要保存继续处理下一个
        if not self.is_new_floder and file_name in os.listdir(self.folder_path): 
            print("该文件已经存在，继续下一个")
            return
        print('开始保存文件')
        f = open(file_name, 'wb')
        f.write(img.content)
        print(file_name, '文件保存成功')
        f.close()

    def get_pic(self):
        print('开始网页get请求')
        r = self.request(self.web_url)
        print('开始获取所有图片标签')
        # 使用BeutifulSoup对得到的html进行解析，所有图片在<div class='article-content'>中，每个照片的url所在标签时<img>
        all_img = BeautifulSoup(r.text, 'lxml').find('div', class_='Viewer_prevItem_McSJ4').find_all('img')
        self.is_new_floder = self.mkdir(self.folder_path)
        os.chdir(self.folder_path)
		
		# 用变量i对照片进行命名
        i = 1;
        for img in all_img:
            url = img['src']
            self.save_img(url, str(i))
            i += 1
            if i>20:
                break

beauty = BeautifulPicture()
beauty.get_pic()

