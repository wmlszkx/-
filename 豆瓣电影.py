from bs4 import BeautifulSoup  # 网页解析，获取数据
import re        # 正则表达式，进行文字匹配
import urllib.request, urllib.error    # 指定URL，获取网页数据
import xlwt      # 进行excel操作



def main():
    baseurl = "https://movie.douban.com/top250?start="# 爬取的网址
    datalist = getdata(baseurl)
    savepath = "豆瓣电影Top250.xls"# 保存
    saveData(datalist, savepath)


# 创建想要提取内容的正则表达式

findLink = re.compile(r'<a href="(.*?)">')  # 影片链接
findImgSrc = re.compile(r'<img.*src="(.*?)"')# 图片
findTitle = re.compile(r'<span class="title">(.*)</span>')# 片名
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')# 影片评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')# 评价人数

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
            datalist.append(data)

 # 将一步电影的所有爬取信息存入datalist列表

    return datalist    # 返回所有电影信息

# 得到指定一个url的网页内容
def askURL(url):
    
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
                            
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

# 保存数据
def saveData(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
    worksheet = workbook.add_sheet('sheet1')  # 创建工作表
    # 创建列名
    col = ("影片链接", "图片链接", "影片中文名称", "影片外文名称", "影片评分", "评价人数")
    for i in range(0, 6):  # 写入列名
        worksheet.write(0, i, col[i]) # 列名
    for i in range(0, 250):  # 写入电影信息
        print("第%d行" %i)
        data = datalist[i]
        for j in range(0, 6):
            worksheet.write(i+1, j, data[j])
    # 保存文件
    workbook.save(savepath)


if __name__ == "__main__":
    # 调用函数
    main()
    print("爬取完毕！")

