import os
import numpy as np
import keras
import time
from keras.layers import LSTM, Dense

data = np.ones((100, 768, 88))
labels = np.ones((100))


def init():
    LSTM_SIZE = 32
    global model

    model = keras.Sequential()

    model.add(LSTM(LSTM_SIZE, input_shape=(None, 88)))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='rmsprop',
                  metrics=['accuracy'])

    model.summary()


def run_learning_batch(data, labels):
    model.fit(data, labels, batch_size=4096, epochs=1)


def learn():
    if not os.path.exists("nn/"):
        os.makedirs("nn/")
    firstd = []
    firstl = []
    first = 1
    f = open("pianotxt/quality.txt", "r")
    labels = f.read().splitlines()
    for a in range(2):
        data = []
        for i in range(len([name for name in os.listdir('pianotxt/') if os.path.isfile('pianotxt/' + name)]) - 1):
            f = open("pianotxt/%d.txt" % (i + 1), "r")
            data.append(f.read().splitlines())
            for j in range(len(data[-1])):
                data[-1][j] = data[-1][j].split(",")
                data[-1][j] = np.asarray([float(k) for k in data[-1][j]])
            data[-1] = np.transpose(np.asarray(data[-1]))
            if len(data) == 100:
                label = np.asarray([labels[i - len(data)+1 + j] for j in range(len(data))])
                data = np.asarray(data)
                run_learning_batch(data, label)
                if first == 1:
                    first = 0
                    firstd = data
                    firstl = label
                data = []
        if len(data) > 0:
            label = np.asarray([labels[i - len(data)+1 + j] for j in range(len(data))])
            data = np.asarray(data)
            run_learning_batch(data, label)
    model.save('nn/1.h5')

    # model = keras.models.load_model('name.h5')

    prediction = model.predict(firstd)

    print(prediction)


def load():
    global model
    model = keras.models.load_model('nn/1.h5')

def evaluate(track):
    global tim
    tim -= time.process_time()
    # f = open("output.txt", "r")
    # track = [f.read().splitlines()]
    track = [track]
    for j in range(len(track[-1])):
    #     track[-1][j] = track[-1][j].split(",")
        track[-1][j] = np.asarray([float(k) for k in track[-1][j]])
    track[-1] = np.transpose(np.asarray(track[-1]))
    track = np.asarray(track)
    result = (model.predict(track))[0]
    tim += time.process_time()
    return result

