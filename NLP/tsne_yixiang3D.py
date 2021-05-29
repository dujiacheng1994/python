from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#数据处理
vector = pd.read_excel('word.xlsx', sheet_name= 0,header = None)
label = vector[0]
X = (vector.drop(vector.columns[0], axis=1, inplace=True))
X = vector.to_numpy()

#建模
tsne = TSNE(n_components=3, init='pca', verbose=2)
embedd = tsne.fit_transform(X)

# 可视化
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(embedd[:71, 0], embedd[:71, 1],embedd[:71, 2])

for i in range(71):
    x = embedd[i][0]
    y = embedd[i][1]
    z = embedd[i][2]
    ax.text(x, y, z, label[i])

plt.show()
plt.savefig('wordplot.png')
