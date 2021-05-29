import numpy as np

def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))  # 创建一个形状为(len(sequences),dimension) 的零矩阵
    for i, sequence in enumerate(sequences):
    results[i, sequence] = 1   # 将results[i] 的指定索引设为1
    return results
x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

# 你还应该将标签向量化，这很简单。
y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')