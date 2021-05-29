import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = []  #语料库
data_file="tfidf_test.txt"

with open(data_file, 'r') as f:
    for line in f:
        corpus.append(" ".join(jieba.cut(line.split(',')[0], cut_all=False)))

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(corpus)

print(tfidf.shape)

words = vectorizer.get_feature_names() #获取所有词语
for i in range(len(corpus)):       #一行/list项 作为一个 document
    print('----Document %d----' % i)
    for j in range(len(words)):
        if tfidf[i,j] > 1e-5:
              print( words[j], tfidf[i,j])