#此程序需要安装jieba，wordcloud库
import jieba
import wordcloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def make_cloud(filepath,bgpath,year):
    f = open(filepath,'r',encoding='utf-8')
    t = f.read()
    f.close()
    ls = jieba.lcut(t)
    txt = ' '.join(ls)
    China_image = np.array(Image.open(bgpath))
    w = wordcloud.WordCloud (font_path = 'c:/windows/Fonts/msyhbd.ttc', width = 1000, height = 700, background_color = 'white', mask = China_image)
    w.generate(txt)
    #重新着色
    image_colors = wordcloud.ImageColorGenerator(China_image)
    plt.imshow(w.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.imshow(China_image, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    w.to_file('Generated_Image/'+year+'wordcloud.png')

year = input("年份(1954-2019)：")
bg = input("背景序号(1-6)：")
filepath = "every_year_repo/"+year+"年.txt"
bgpath = "Background/"+"China"+str(bg)+".jpg"

make_cloud(filepath,bgpath,year)

