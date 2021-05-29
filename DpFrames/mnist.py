from tensorflow import keras as kr

(train_images, train_labels), (test_images, test_labels) = kr.datasets.mnist.load_data()
network = kr.models.Sequential()
network.add(kr.layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(kr.layers.Dense(10, activation='softmax'))

network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

train_labels = kr.utils.to_categorical(train_labels)
test_labels = kr.utils.to_categorical(test_labels)

network.fit(train_images, train_labels, epochs=5, batch_size=128)

test_loss, test_acc = network.evaluate(test_images, test_labels)
print('test_acc:', test_acc)

# digit = train_images[4]
# import matplotlib.pyplot as plt
# plt.imshow(digit, cmap=plt.cm.binary)
# plt.show()
#
# my_slice = train_images[:, 7:-7, 7:-7]
# batch = train_images[:128]

# word_index = imdb.get_word_index()
# reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
# decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])