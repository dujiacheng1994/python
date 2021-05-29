from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图

plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

#数据处理
vector = pd.read_excel('word.xlsx', sheet_name= 0,header = None)
label = vector[0]
X = (vector.drop(vector.columns[0], axis=1, inplace=True))
X = vector.to_numpy()

#建模
tsne = TSNE(n_components=2, init='pca', verbose=1)
embedd = tsne.fit_transform(X)

x_index=[]
y_index=[]
item_num = 71
for i in range(item_num):
    x = embedd[i][0]-min(embedd[:item_num, 0])
    y = embedd[i][1]-min(embedd[:item_num, 1])
    x_index.append(x)
    y_index.append(y)

# 可视化
plt.figure(figsize=(12, 12))
# plt.scatter(embedd[:71, 0], embedd[:71, 1])
plt.scatter(x_index,y_index)
for i in range(item_num):
    plt.text(x_index[i], y_index[i], label[i])

plt.savefig('wordplot2D.png')
plt.show()

#3D云展示
import math
#定义极坐标转直角坐标函数
def uvToxyz(u, v, r):
    wd = (u + 90) * math.pi / 180
    jd = v * math.pi / 180
    x = -r * math.cos(jd) * math.cos(wd)
    y = -r * math.sin(jd)
    z = r * math.cos(jd) * math.sin(wd)
    return x, y, z
#将二维转成2:1比例图以适应转球面
xx=[];yy=[] #二维坐标2：1版
for item in x_index:
    xx.append(item)
for item in y_index:
    yy.append(item / 2.0)

#定义图宽与高2:1
if (max(xx)-min(xx))>(max(yy)-min(yy)):
    W=(max(xx)-min(xx))
    H=W/2
else:
    W=(max(yy)-min(yy))
    H=W/2
r=10
#计算将点的直角坐标
x3d=[]; y3d=[]; z3d=[]
for i in range(len(x_index)):
    u = (360.0 * xx[i] / W) -180
    v = (180.0 * yy[i] / H) -90
    x,y,z=uvToxyz(u,v,r)
    x3d.append(x)
    y3d.append(y)
    z3d.append(z)
#绘出标签点云图及其标签
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(x3d, y3d, z3d)
for i in range(71):
    x = x3d[i]
    y = y3d[i]
    z = z3d[i]
    ax.text(x, y, z, label[i])

#读取AILab文件
# from gensim.models.word2vec import Word2VecKeyedVectors
# file = "AIlab.txt"
# model = Word2VecKeyedVectors.load_word2vec_format(file, binary=False,unicode_errors='ignore')

#与某个词最相近的词

i= 46
word = label[i]
print(u'与%s最相近的5个词' % word)
req_count=5  #求出5个与之相近的词
sim_list=[]
for key in model.similar_by_word(word,topn=100):
    if len(key[0])==len(word):   #key[0]应该就表示某个词
        req_count-=1
        print(key[0],key[1])  #某一个词,某一个词出现的概率
        sim_list.append(key[0])
        if req_count==0:
            break
#绘制联想点
i=11
deg = 6
u = (360.0 * xx[i] / W) -180 -deg
v = (180.0 * yy[i] / H) -90 -deg
x,y,z=uvToxyz(u,v,r)
ax.scatter(x,y,z,c='r')
ax.text(x, y, z, sim_list[0])

u = (360.0 * xx[i] / W) -180 +deg
v = (180.0 * yy[i] / H) -90 -deg
x,y,z=uvToxyz(u,v,r)
ax.scatter(x,y,z,c='r')
ax.text(x, y, z, sim_list[1])

u = (360.0 * xx[i] / W) -180 -deg
v = (180.0 * yy[i] / H) -90 +deg
x,y,z=uvToxyz(u,v,r)
ax.scatter(x,y,z,c='r')
ax.text(x, y, z, sim_list[2])

u = (360.0 * xx[i] / W) -180 +deg
v = (180.0 * yy[i] / H) -90 +deg
x,y,z=uvToxyz(u,v,r)
ax.scatter(x,y,z,c='r')
ax.text(x, y, z, sim_list[3])