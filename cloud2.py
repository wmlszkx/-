import jieba
import sqlite3 

con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = 'select instroduction from movie250'
data = cur.execute(sql)
text = ""  # 初始化text为空字符串，后续将文本数据逐步添加到其中

# 将查询结果中的文本数据添加到text中
for item in data:
    text += item[0]

cur.close()
con.close()

cut = jieba.cut(text)
print("分词结果：", list(cut))
