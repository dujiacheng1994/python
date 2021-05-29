from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图
import math
from gensim.models.word2vec import Word2VecKeyedVectors

#读取AILab数据，这一步需要数十分钟
def readAIlab(path="AIlab.txt"):
    model = Word2VecKeyedVectors.load_word2vec_format(path, binary=False, unicode_errors='ignore')
    return model

if __name__ == '__main__':
    # X,label = readData('word.xlsx')
    # x_index, y_index = build_model(X,label)
    # x3d, y3d, z3d = D2toD3(x_index, y_index)
    # drawplain(x_index, y_index,label)
    # drawSphere(x3d, y3d, z3d, label)
    model = readAIlab(r'D:\after.txt')  #读取AILab数据，这一步需要数十分钟，及至少16G内存，以下步骤依赖于此步
    # print(find_Similar(model,'月亮'))  #示例：获取'月亮'的相似词
    # print(get_similarity(model,'小鱼','皇后'))