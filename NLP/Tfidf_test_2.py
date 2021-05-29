from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
corpus = ["我 来到 北京 清华大学",  # 第一类文本切词后的结果，词之间以空格隔开
          "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果
          "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
          "我 爱 北京 天安门"]  # 第四类文本的切词结果

vec = CountVectorizer()  # 初始化CountVectorizer, 该类会将文本中的词语转换为词频矩阵, 矩阵元素a[i][j] 表示j词在i类文本下的词频
tf = TfidfTransformer()  # 初始化TfidfTransformer, 该类会统计每个词语的tf-idf权值

X = vec.fit_transform(corpus)  # 该fit_transform是将文本转为词频矩阵
tfidf = tf.fit_transform(X)  # 该fit_transform是计算tf-idf

word = vec.get_feature_names()  # 获取词袋模型中的所有词语
weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    for j in range(len(word)):
        print(word[j], weight[i][j])