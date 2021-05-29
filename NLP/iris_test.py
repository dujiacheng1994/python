# Python version
import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy
print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas
print('pandas: {}'.format(pandas.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))

# Load libraries
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection  #模型比较和选择包
from sklearn.metrics import classification_report  #将主要分类指标以文本输出
from sklearn.metrics import confusion_matrix #计算混淆矩阵，主要来评估分类的准确性
from sklearn.metrics import accuracy_score #计算精度得分
from sklearn.linear_model import LogisticRegression #线性模型中的逻辑回归
from sklearn.tree import DecisionTreeClassifier #树算法中的决策 a树分类包
from sklearn.neighbors import KNeighborsClassifier #导入最近邻算法中的KNN最近邻分类包
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis #判别分析算法中的线性判别分析包
from sklearn.naive_bayes import GaussianNB #朴素贝叶斯中的高斯朴素贝叶斯包
from sklearn.svm import SVC  #支持向量机算法中的支持向量分类包

# Load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names) #读取csv数据

# shape
print(dataset.shape)
# head
print(dataset.head(20))
# descriptions
print(dataset.describe())
# class distribution
print(dataset.groupby('class').size())
# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.show()
# histograms
dataset.hist()
plt.show()
# scatter plot matrix
scatter_matrix(dataset)
plt.show()
