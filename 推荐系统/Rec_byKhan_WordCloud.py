import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ratings = pd.read_csv('ratings.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'movie_id', 'rating'])
users = pd.read_csv('users.csv', sep='\t', encoding='latin-1',usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])
movies = pd.read_csv('movies.csv', sep='\t', encoding='latin-1', usecols=['movie_id', 'title', 'genres'])

#画出电影名所用单词的文字云
from wordcloud import WordCloud, STOPWORDS
# Create a wordcloud of the movie titles
movies['title'] = movies['title'].fillna("").astype('str')
title_corpus = ' '.join(movies['title'])
title_wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black', height=2000, width=4000).generate(title_corpus)
# Plot the wordcloud
plt.figure(figsize=(16, 8))
plt.imshow(title_wordcloud)
plt.axis('off')
plt.show()

#画电影评分1-5各频数的条形图
import seaborn as sns
sns.set_style('whitegrid')
sns.set(font_scale=1.5)
sns.distplot(ratings['rating'].fillna(ratings['rating'].median()))
plt.show()

# merge三个表movies,rating,users
dataset = pd.merge(pd.merge(movies, ratings), users)
# 显示20个最高评分电影
dataset[['title', 'genres', 'rating']].sort_values('rating', ascending=False).head(20)

# 建立类型关键词的census（总体词频数据），用于求IDF
genre_labels = set()
for s in movies['genres'].str.split('|').values:
    genre_labels = genre_labels.union(set(s))


# 统计词频
def count_word(dataset, ref_col, census):
    keyword_count = dict()
    for s in census:
        keyword_count[s] = 0
    for census_keywords in dataset[ref_col].str.split('|'):
        if type(census_keywords) == float and pd.isnull(census_keywords):
            continue
        for s in [s for s in census_keywords if s in census]:
            if pd.notnull(s):
                keyword_count[s] += 1

    # convert the dictionary in a list to sort the keywords by frequency
    keyword_occurences = []
    for k, v in keyword_count.items():
        keyword_occurences.append([k, v])
    keyword_occurences.sort(key=lambda x: x[1], reverse=True)
    return keyword_occurences, keyword_count


# dum为无序dict型，keyword_occurences为有序list(依类型热度排序)
keyword_occurences, dum = count_word(movies, 'genres', genre_labels)
print(keyword_occurences[:5])

# genres用于构建词云
genres = dict()
trunc_occurences = keyword_occurences[0:18]  #截取前18个大类
for s in trunc_occurences:
    genres[s[0]] = s[1]  #将元素[Drama,1603]变成<Drama,1603>的key-value型dict

# 建词云
genre_wordcloud = WordCloud(width=1000, height=400, background_color='white')
genre_wordcloud.generate_from_frequencies(genres)

# 画词云
f, ax = plt.subplots(figsize=(16, 8))
plt.imshow(genre_wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()