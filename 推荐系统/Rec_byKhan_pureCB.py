import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
ratings = pd.read_csv('ratings.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'movie_id', 'rating'])
users = pd.read_csv('users.csv', sep='\t', encoding='latin-1',usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])
movies = pd.read_csv('movies.csv', sep='\t', encoding='latin-1', usecols=['movie_id', 'title', 'genres'])

movies['genres'] = movies['genres'].str.split('|')
movies['genres'] = movies['genres'].fillna("").astype('str')

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')

tfidf_matrix = tf.fit_transform(movies['genres'])  #传入每个电影的类别字符串作为n个文档，训练tf-idf稀疏矩阵
words = tf.get_feature_names() # 列出文档的关键词名称，先得fit_transform

tfidf_matrix_dense = tfidf_matrix.todense()  # [3883*127],每列代表一个关键词drama，一列中各行代表3883个电影document中关键词drama的tf-idf值
#i = np.matrix('1,2;3,4')  #分号换行
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)  # 矩阵相乘

titles = movies['title']
indices = pd.Series(movies.index, index=movies['title'])  #建立第二数组，参数为[data,index]，从[0,'Toy Story (1995)']数组 -> [ 'Toy Story (1995)'，0] 配合titles数组便于按名检索

# 函数：传入电影标题，返回相似电影标题
def genre_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))   #cosine_sim[idx]为index与其它电影的相似度向量，enumerate用于取每个项：(数据下标，数据)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  #simscore格式为<0，0.99999>。第二个key参数需要是个函数，定义排序所用的key,此处用sim_scores[1]即相似度排序
    sim_scores = sim_scores[1:21] #取除自己之外的前20个相似电影<0，0.99999>
    movie_indices = [i[0] for i in sim_scores]  #取前20电影的index
    return titles.iloc[movie_indices]  #依index取前20电影的标题

genre_recommendations('Good Will Hunting (1997)').head(20)
