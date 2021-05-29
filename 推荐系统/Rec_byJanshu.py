import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('ml-100k/u.data', sep='\t',names=['user_id','item_id','rating','timestamp'])
#print(df.head())
movie_titles = pd.read_csv('ml-100k/u.item',sep='|',names=['item_id','movie title','release date','video release date','IMDb URL','unknown','Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western'],encoding = "ISO-8859-1",)
#movie_titles.head()
df = pd.merge(df, movie_titles, on='item_id') #依item_id合并（这两向量相同）
df.head()

df.describe() #维度、均值等统计量
ratings = pd.DataFrame(df.groupby('movie title')['rating'].mean())
ratings.head()
ratings['number_of_ratings'] = df.groupby('movie title')['rating'].count()
ratings.head()

import matplotlib
import matplotlib.pyplot as plt

ratings['rating'].hist(bins=50)
plt.show()
ratings['number_of_ratings'].hist(bins=60)
plt.show()
# 绘制散点图
import seaborn as sns
sns.jointplot(x='rating', y='number_of_ratings', data=ratings)
plt.show()
movie_matrix = df.pivot_table(index='user_id', columns='movie title', values='rating')
movie_matrix.head()

ratings.sort_values('number_of_ratings', ascending=False).head(10)
AFO_user_rating = movie_matrix['Air Force One (1997)']
contact_user_rating = movie_matrix['Contact (1997)']

AFO_user_rating.head()
contact_user_rating.head()

similar_to_air_force_one=movie_matrix.corrwith(AFO_user_rating)
similar_to_air_force_one.head()
similar_to_contact = movie_matrix.corrwith(contact_user_rating)
similar_to_contact.head()

corr_contact = pd.DataFrame(similar_to_contact, columns=['Correlation'])
corr_contact.dropna(inplace=True)
corr_contact.head()
corr_AFO = pd.DataFrame(similar_to_air_force_one, columns=['correlation'])
corr_AFO.dropna(inplace=True)
corr_AFO.head()

corr_AFO = corr_AFO.join(ratings['number_of_ratings'])
corr_contact = corr_contact.join(ratings['number_of_ratings'])
corr_AFO .head()
corr_contact.head()

corr_AFO[corr_AFO['number_of_ratings'] > 100].sort_values(by='correlation', ascending=False).head(10)
corr_contact[corr_contact['number_of_ratings'] > 100].sort_values(by='Correlation', ascending=False).head(10)