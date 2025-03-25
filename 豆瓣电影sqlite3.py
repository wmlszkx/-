# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 20:38:25 2022

@author: 邹可馨
"""

from bs4 import BeautifulSoup      # 网页解析，获取数据
import re        # 正则表达式，进行文字匹配
import urllib.request, urllib.error    # 指定URL，获取网页数据
import sqlite3      # 进行数据库操作


def main():
    baseurl = "https://movie.douban.com/top250?start="# 爬取的网址
    datalist = getdata(baseurl)
    dbpath = "movie.db"# 保存
    saveData(datalist,dbpath)


# 创建想要提取内容的正则表达式

findLink = re.compile(r'<a href="(.*?)">')  # 影片链接
findImgSrc = re.compile(r'<img.*src="(.*?)"')# 图片
findTitle = re.compile(r'<span class="title">(.*)</span>')# 片名
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')# 影片评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')# 评价人数
findinq=re.compile(r'<span class="inq">(.*)</span>')#概况
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)#相关内容

# 爬取网页
def getdata(baseurl):
    datalist = []
    for i in range(0, 10):
        n = str(i*25)   # 页数
        url = baseurl + n  # 每一页的网址
        html = askURL(url)  # 访问每一个网页的内容
        soup = BeautifulSoup(html,"html.parser")# 解析数据
        # 找到所要信息所在的网页中的位置
        for item in soup.find_all('div', class_="item"):
            data = []  # 保存一部电影的全部信息
            item = str(item)
            # 获取到影片的超链接
            link = re.findall(findLink, item)[0]   # 获取电影链接
            data.append(link)  # 添加电影链接
            imgSrc = re.findall(findImgSrc, item)[0]  # 获取图片链接
            data.append(imgSrc)
            title = re.findall(findTitle, item)  # 获取电影名称
            if(len(title) == 2): # 区分中文名称和外文名称
                data.append(title[0])
                otitle = title[1].replace("/", "")
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ')  # 如果没有外文名称则用空格占位，防止混乱
            rating = re.findall(findRating, item)[0]   # 获取评分
            data.append(rating)
            judge = re.findall(findJudge, item)[0]   # 获取评价人数
            data.append(judge)
            inq=re.findall(findinq,item)
            if len(inq)!=0:
                inq=inq[0].replace("。","")#去句号
                data.append(inq)
            else:
                data.append("   ")
            bd=re.findall(findBd,item)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd=re.sub('/'," ",bd)
            bd=re.sub('\xa0',' ',bd)
            data.append(bd.strip())
            datalist.append(data)# 将一步电影的所有爬取信息存入datalist列表
    print(datalist)
    return datalist    # 返回所有电影信息

# 得到指定一个url的网页内容
def askURL(url):
    
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

# 初始化数据库
def init_db(dbpath):
    sql='''
    create table movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )'''
    conn=sqlite3.connect(dbpath)
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def saveData(datalist, dbpath):
   init_db(dbpath)
   conn=sqlite3.connect(dbpath)
   cur=conn.cursor()
   
   for data in datalist:
       for index in range(len(data)):
           if index==4 or index==5:
               continue
           data[index]= '"'+str(data[index])+'"'
       sql='''
               insert into movie250(
               info_link,pic_link,cname,ename,score,rated,instroduction,info)
               values(%s)'''%",".join(data)
       cur.execute(sql)
       conn.commit()
   cur.close()
   conn.close()

if __name__ == "__main__":
    main()#调用函数
    print("爬取完毕！")