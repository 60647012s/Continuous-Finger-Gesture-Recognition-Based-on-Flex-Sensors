from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from LIB.TrainPreprocess.TRAINPRE import *
from LIB.TrainPreprocess.TRAINPRE_UTILS import *
# from LIB.MODEL_GRU import *
from LIB.MODEL_PAIRNET import *
import tensorflow as tf
import keras.backend as K
import os

'''
  新增路徑
'''
def addFolder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


'''
  MODELPATH 檔案路徑宣告：
  時間_訓練次數_訓練資料集_隱藏層輸出維度_window的大小_NCu/Cu
'''
# MODELPATH = "201907020000_10_trainData1_128_60_Cu"
MODELPATH = "201909091922_10_trainData1_128_60_Cu"
MODELNUM = int(MODELPATH.split('_')[1])
DATASET = MODELPATH.split('_')[2]
HDIM = int(MODELPATH.split('_')[3])
WSIZE = int(MODELPATH.split('_')[4])
CudaSwitch = 1
if MODELPATH.split('_')[5] == "NCu":
    CudaSwitch = 0

AXIS = 3  # 3 根手指
GESTURECLASS = 4  # 4 個手勢


'''
  忽略警告訊息
'''
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


'''
  資料前處理
  preprocessing & preprocessing_unit
'''
train, train_label = getSamples(getFiles('train1&2_test2/' + DATASET))
x_train, y_train, x_test, y_test = getTrain(train, train_label, WSIZE, GESTURECLASS, AXIS)


y_train = y_train[:, -1, :]
y_test = y_test[:, -1, :]

for countTime in range(MODELNUM):
    addFolder('model/' + MODELPATH)
    modelName = 'model/' + MODELPATH + '/' + str(countTime + 1) + '_' + MODELPATH + '.h5'
    model = build_model(HDIM, AXIS, GESTURECLASS, WSIZE, CudaSwitch)

    # GPU使用限制：train 須放在 model 之後，fit 之前
    # gpu_options 設定 gpu 用量， device_count 設定 GPU 啟用編號，log_device_placement 印出詳細資訊
    gpu_option = tf.GPUOptions(allow_growth=True, per_process_gpu_memory_fraction=0.6)
    if CudaSwitch == 1:
        config = tf.ConfigProto(gpu_options=gpu_option)
    else:
        config = tf.ConfigProto(gpu_options=gpu_option,
                                device_count={'GPU': 0},
                                log_device_placement=False)
    sess = tf.Session(config=config)
    K.set_session(sess)

    lr = ReduceLROnPlateau(patience=30, factor=0.5, epsilon=0.001, min_lr=0.00001, verbose=0)
    c = ModelCheckpoint(modelName, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False,
                        mode='auto', period=1)
    history = model.fit(x_train, y_train,
                        batch_size=128,
                        epochs=50,
                        validation_data=(x_test, y_test),
                        callbacks=[c, lr],
                        verbose=0)

    K.clear_session()
