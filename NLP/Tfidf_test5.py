#类1 ：CountVectorizer 将文本文档集合转换为 词频计数 的稀疏矩阵
from sklearn.feature_extraction.text import CountVectorizer

corpus = ['This is the first document.',
          'This document is the second document.',
          'And this is the third one.',
          'Is this the first document?']

vectorizer = CountVectorizer()  # 初始化，()这里不提供先验词典
# vectorizer.fit(corpus)			# 先fit训练传入的文本数据
# X = vectorizer.transform(corpus)		# 然后对文本数据进行标记并转换为稀疏计数矩阵
X = vectorizer.fit_transform(corpus)  # 可以fit、transform一起使用替代上面的两行

print(vectorizer.get_feature_names())  # 获得模型直接分析数据找到的词汇量（上面不重复单词的集合）
print(X.toarray())  # 直接打印X输出的是每个词的位置矩阵[

# ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
# [[0 1 1 1 0 0 1 0 1]  # 4行 数据样本
#  [0 2 0 1 0 1 1 0 1]  # 9列 特征单词
#  [1 0 0 1 1 0 1 1 1]
#  [0 1 1 1 0 0 1 0 1]]


#类2 ：TfidfTransformer 将 词频计数矩阵 转换为 标准化的 tf 或 tf-idf 表示
from sklearn.feature_extraction.text import TfidfTransformer

transform = TfidfTransformer()  # 初始化，使用TF-IDF（词频、逆文档频率）应用于稀疏矩阵
Y = transform.fit_transform(X)  # 使用上面CountVectorizer处理后的 X 数据
print(Y.toarray())  # 输出转换为tf-idf后的 Y 矩阵，同样直接打印 Y 输出每个数据的位置
print(vectorizer.get_feature_names())  # 打印特征名


#类3 ： TfidfVectorizer 相当于两者的结合使用
from sklearn.feature_extraction.text import TfidfVectorizer

VT = TfidfVectorizer()  # 先后调用CountVectorizer和TfidfTransformer两种方法（简化了代码，但运算思想还是不变）
result = VT.fit_transform(corpus)  #同名fit_transform()方法，直接得出tf_idf矩阵
print(result.toarray())
print(VT.get_feature_names())
