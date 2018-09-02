import numpy as np
import keras as k
from keras.layers import LSTM, Dense

data = np.ones((100, 768, 88))
labels = np.ones((100))

LSTM_SIZE = 32

model = k.Sequential()

model.add(LSTM(LSTM_SIZE, input_shape=(None, 88)))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='rmsprop',
              metrics=['accuracy'])

model.summary()

model.fit(data, labels, batch_size=4096, epochs=2)

model.save('name.h5')

loaded_model = k.models.load_model('name.h5')

prediction = loaded_model.predict(data)

print(prediction[:20])


