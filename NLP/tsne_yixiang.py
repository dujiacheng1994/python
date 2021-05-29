from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#数据处理
vector = pd.read_excel('word.xlsx', sheet_name= 0,header = None)
label = vector[0]
X = (vector.drop(vector.columns[0], axis=1, inplace=True))
X = vector.to_numpy()

#建模
tsne = TSNE(n_components=2, init='pca', verbose=1)
embedd = tsne.fit_transform(X)

# 可视化
plt.figure(figsize=(24, 12))
plt.scatter(embedd[:71, 0], embedd[:71, 1])

x_index=[]
y_index=[]
for i in range(71):
    x = embedd[i][0]
    y = embedd[i][1]
    x_index.append(x)
    y_index.append(y)
    plt.text(x, y, label[i])

plt.savefig('wordplot2D.png')
plt.show()

# a=vector.loc[3,:]
# b=vector.loc[8,:]
#aa=np.array(a)
#bb=np.array(b)
#res=np.dot(aa,bb)/np.linalg.norm(aa)/np.linalg.norm(bb)

