#此程序需要安装jieba，wordcloud库
import jieba
import wordcloud
import PIL
from PIL import ImageTk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

root = Tk()

root.title('生成词云')
Label(root, text='年份 :').grid(row=0, column=0)  # 对Label内容进行 表格式 布局
Label(root, text='背景序号 :').grid(row=1, column=0)

img_gif = PhotoImage()
label_img = Label(root, image = img_gif)
label_img.grid(row=0,column=2,rowspan=10,columnspan=10,sticky=N)


v1 = StringVar()  # 设置变量 .
v2 = StringVar()
e1 = Entry(root, textvariable=v1)  # 用于储存 输入的内容
e2 = Entry(root, textvariable=v2)
e1.grid(row=0, column=1, padx=10, pady=5)  # 进行表格式布局 .
e2.grid(row=1, column=1, padx=10, pady=5)


def make_cloud():
    year = e1.get()
    bg = e2.get()
    filepath = "every_year_repo/" + year + "年.txt"
    bgpath = "Background/" + "China" + str(bg) + ".jpg"
    f = open(filepath,'r',encoding='utf-8')
    t = f.read()
    f.close()
    ls = jieba.lcut(t)
    txt = ' '.join(ls)
    China_image = np.array(PIL.Image.open(bgpath))
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

    a=PIL.Image.open(r'Generated_Image/'+year+'wordcloud.png')
    a = a.resize((609, 512),PIL.Image.ANTIALIAS)
    a.save("current.png")
    url=r"current.png"
    img_pil = PIL.Image.open(url)
    img = ImageTk.PhotoImage(img_pil)
    label_img.config(image=img)
    label_img.image = img  # keep a reference
    root.update_idletasks()

Button(root, text='制作词云', width=10, command=make_cloud).grid(row=3, column=0, sticky=W, padx=10, pady=5)
Button(root, text='退出', width=10, command=root.quit).grid(row=3, column=1, sticky=E, padx=10, pady=5)
mainloop()







