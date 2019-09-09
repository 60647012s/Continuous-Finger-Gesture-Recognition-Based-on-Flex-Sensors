import numpy as np
import random
from keras.utils.np_utils import to_categorical
from LIB.TrainPreprocess.TRAINPRE_UTILS import *




def getTrain(train, train_label, wLength, classNUM, axis):
    data_x, class_y = [], []

    for i in range(len(train)):
        if len(train[i]) != len(train_label[i]) or len(train[i]) == 0:
            continue

        l = len(train[i])

        for j in range(0, (l - wLength), 1):  #改為交疊一次看 wLength 個
            data_x.append(train[i][j:j+wLength])
            class_y.append(to_categorical(train_label[i][j:j+wLength], classNUM))


    c = list(zip(data_x, class_y))
    random.shuffle(c)
    data_x, class_y = zip(*c)

    data_x = np.array(data_x).reshape(len(data_x), wLength, axis).astype(float)
    class_y = np.array(class_y).reshape(len(class_y), wLength, classNUM).astype(int)


    l = int(len(data_x) * 0.85)
    x_train = data_x[:l]
    x_test = data_x[l:]
    y_train = class_y[:l]
    y_test = class_y[l:]

    c = list(zip(x_train, y_train))
    random.shuffle(c)
    x_train, y_train = zip(*c)

    x_train = np.array(x_train).reshape(len(x_train), wLength, axis)
    x_test = np.array(x_test).reshape(len(x_test), wLength, axis)
    y_train = np.array(y_train).reshape(len(y_train), wLength, classNUM)
    y_test = np.array(y_test).reshape(len(y_test), wLength, classNUM)

    return x_train, y_train, x_test, y_test

if __name__ == '__main__':
    train, train_label = getSamples(getFiles('目標檔案絕對路徑'))
    x_train, y_train, x_test, y_test = getTrain(train, train_label, 60, 4, 3)
