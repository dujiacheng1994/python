import numpy as np
import pandas as pd

header = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('ml-100k/u.data', sep='\t', names=header)

n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]
print('Number of users = ' + str(n_users) + ' | Number of movies = ' + str(n_items))  # 用户数与item数

from sklearn.model_selection import train_test_split  # Cross Validation 样本分割

train_data, test_data = train_test_split(df, test_size=0.25)

# Create two user-item matrices, one for training and another for testing
train_data_matrix = np.zeros((n_users, n_items))  # 创建numpy零矩阵
for line in train_data.itertuples():
    train_data_matrix[line[1] - 1, line[2] - 1] = line[3]  # 由多行三元组记录<user_id,item_id,rating> 转化为（用户评分）矩阵 [userid,itemid]->rating

from sklearn.metrics.pairwise import pairwise_distances

user_similarity = pairwise_distances(train_data_matrix, metric='cosine')  #计算train_data中用户之间的余弦距离（1-余弦相似度） !还要除以norm
item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')


def predict(ratings, similarity, type='item'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        # You use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array(
            [np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])   #向量点积a.dot(b)=a.*b
    return pred

item_prediction = predict(train_data_matrix, item_similarity, type='item')
user_prediction = predict(train_data_matrix, user_similarity, type='user')

from sklearn.metrics import mean_squared_error
from math import sqrt
def rmse (prediction,ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))

print ('User-based CF RMSE: ' + str(rmse(user_prediction, train_data_matrix)))
print ('Item-based CF RMSE: ' + str(rmse(item_prediction, train_data_matrix)))


sparsity = round(1.0 - len(df) / float(n_users * n_items), 3)
print('The sparsity level of MovieLens100K is ' + str(sparsity * 100) + '%')
