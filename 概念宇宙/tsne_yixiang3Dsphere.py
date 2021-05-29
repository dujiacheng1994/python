from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图
import math
from gensim.models.word2vec import Word2VecKeyedVectors

# 读取excel数据
def readData(path = 'word.xlsx'):
    vector = pd.read_excel(path, sheet_name=0, header=None)
    label = vector[0]
    X = (vector.drop(0, axis=1, inplace=True))
    X = vector.to_numpy()
    return X,label

# tsne建模
def build_model(X,label):
    tsne = TSNE(n_components=2, init='pca', verbose=1)
    embedd = tsne.fit_transform(X)
    x_index = []  #每个意象的二维坐标
    y_index = []
    item_num = label.__len__()
    for i in range(item_num):
        x = embedd[i][0] - min(embedd[:item_num, 0])   #将坐标全部移到第一象限
        y = embedd[i][1] - min(embedd[:item_num, 1])
        x_index.append(x)
        y_index.append(y)
    return x_index,y_index

# 3D云展示

# 定义极坐标转直角坐标函数
def uvToxyz(u, v, r):
    wd = (u + 90) * math.pi / 180
    jd = v * math.pi / 180
    x = -r * math.cos(jd) * math.cos(wd)
    y = -r * math.sin(jd)
    z = r * math.cos(jd) * math.sin(wd)
    return x, y, z

def D2toD3(x_index,y_index):
    # 将二维转成2:1比例图以适应转球面
    xx = []
    yy = []  # 二维坐标2：1版
    for item in x_index:
        xx.append(item)
    for item in y_index:
        yy.append(item / 2.0)
    # 定义图宽与高2:1
    if (max(xx) - min(xx)) > (max(yy) - min(yy)):
        W = (max(xx) - min(xx))
        H = W / 2
    else:
        W = (max(yy) - min(yy))
        H = W / 2
    r = 10 #todo:该参数为球半径，可任意选取
    # 计算点的直角坐标
    x3d = []
    y3d = []
    z3d = []
    for i in range(len(x_index)):
        u = (360.0 * xx[i] / W) - 180
        v = (180.0 * yy[i] / H) - 90
        x, y, z = uvToxyz(u, v, r)
        x3d.append(x)
        y3d.append(y)
        z3d.append(z)
    return x3d,y3d,z3d

def drawplain(x_index,y_index, label):  #二维可视化
    plt.figure(figsize=(12, 12))
    plt.scatter(x_index, y_index)
    for i in range(label.__len__()):
        plt.text(x_index[i], y_index[i], label[i])
    #plt.savefig('意象宇宙2D.png')
    plt.show()

# 三维可视化
def drawSphere(x3d,y3d,z3d,label):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x3d, y3d, z3d)
    for i in range(label.__len__()):
        x = x3d[i]
        y = y3d[i]
        z = z3d[i]
        ax.text(x, y, z, label[i])

#读取AILab数据，这一步需要数十分钟
def readAIlab(path="AIlab.txt"):
    model = Word2VecKeyedVectors.load_word2vec_format(path, binary=False, unicode_errors='ignore')
    return model

#联想，获取与词word相似的n个词
def find_Similar(model,word,n=5):
    sim_list=[]
    for key in model.similar_by_word(word,topn=100):
        if len(key[0])==len(word):
            n-=1
            #print(key[0],key[1])  #某一个词,某一个词出现的概率
            sim_list.append(key[0])
            if n==0:
                break
    return sim_list
#获取相似度
def get_similarity(model,word1,word2):
    try:
        sim = model.similarity(word1, word2)
    except KeyError:
        sim = 0
    return sim


if __name__ == '__main__':
    X,label = readData('word.xlsx')
    x_index, y_index = build_model(X,label)
    x3d, y3d, z3d = D2toD3(x_index, y_index)
    drawplain(x_index, y_index,label)
    drawSphere(x3d, y3d, z3d, label)
    # model = readAIlab('AIlab.txt')  #读取AILab数据，这一步需要数十分钟，及至少16G内存，以下步骤依赖于此步
    # print(find_Similar(model,'月亮'))  #示例：获取'月亮'的相似词
    # print(get_similarity(model,'小鱼','皇后'))