import keras
from keras.models import Model
from keras.layers import *

def build_model(hDim, axis, classNum, wSize, CudaSwitch):
    input1 = Input(shape=(wSize, axis))

    # PairNet
    #out = BatchNormalization()(input1)
    out = Conv1D(256, 3, activation='relu')(input1)         #48
    out = BatchNormalization()(out)
    out = Conv1D(256, 2, strides=2, activation='relu')(out) #24
    out = BatchNormalization()(out)
    out = Conv1D(256, 2, strides=2, activation='relu')(out) #12
    out = BatchNormalization()(out)
    out = Conv1D(512, 2, strides=2, activation='relu')(out) #6
    out = BatchNormalization()(out)
    out = Conv1D(512, 2, strides=2, activation='relu')(out) #3
    out = BatchNormalization()(out)
    out = GlobalAveragePooling1D()(out)
 
    out = Dense(classNum, activation='softmax')(out)

    model = Model(inputs=input1, outputs=out)
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    model.summary()
    return model
