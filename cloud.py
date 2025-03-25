import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3 

con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = 'select instroduction from movie250'
data = cur.execute(sql)
text = " "
for item in data:
    text = text + item[0]
cur.close()
con.close()

cut = jieba.cut(text)
string='   '.join(cut)

# 绘图
img = Image.open(r'.\static\assets\img\831.jpg')
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="STXINWEI",
    max_words=831,  # 调整此参数以显示更多的词
    width=500,       # 调整图片宽度以显示更多词
    height=800,      # 调整图片高度以显示更多词
    collocations=False,  # 不显示双词搭配
    stopwords=None       # 可以设置停用词
)

wc.generate_from_text(string)

#fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
plt.savefig(r'.\static\assets\img\word.jpg', dpi=1500)
