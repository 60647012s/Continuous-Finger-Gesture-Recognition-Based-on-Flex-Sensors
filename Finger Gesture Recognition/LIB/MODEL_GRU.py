import keras
from keras.models import Model
from keras.layers import Dense, Activation
from keras.layers import CuDNNGRU, GRU, Input


def build_model(hDim, axis, classNum, wSize, CudaSwitch):
    input1 = Input(shape=(wSize, axis))

    if CudaSwitch == 1:
        out = CuDNNGRU(hDim)(input1)
    else:
        out = GRU(hDim, recurrent_activation='sigmoid', use_bias=True)(input1)
    out = Dense(classNum)(out)
    out = Activation('softmax')(out)

    model = Model(inputs=input1, outputs=out)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


if __name__ == '__main__':
    model = build_model(128, 3, 4, 60, 1)
    model.summary()
