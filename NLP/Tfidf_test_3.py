from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

document = ["I have a pen.", "I have an apple."]  # 字符串list,每个元素为1个document

tfidf_model = TfidfVectorizer().fit(document)    # 建立tfidf模型，vocabulary表示词频
sparse_result2 = TfidfVectorizer().transform(document)
sparse_result = tfidf_model.transform(document)  # 得到tfidf模型的稀疏矩阵表示法

print(sparse_result)
print(sparse_result.todense())  # 转化为更直观的一般矩阵
print(tfidf_model.vocabulary_)  # 词语与列的对应关系,
