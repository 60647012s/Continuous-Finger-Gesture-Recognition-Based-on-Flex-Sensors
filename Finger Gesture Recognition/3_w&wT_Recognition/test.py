from LIB.ORDERACCURACY import OrderAccuracy
from keras.models import load_model
import os
from os import listdir, path
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

TESTPATH = 'train1&2_test2/testData2/'
# MODELPATH = "201907020000_10_trainData1_128_60_Cu"
MODELPATH = "201907020000_10_trainData2_128_60_Cu"
MODELNUM = int(MODELPATH.split('_')[1])
DATASET = MODELPATH.split('_')[2]
HDIM = int(MODELPATH.split('_')[3])
WSIZE = int(MODELPATH.split('_')[4])
AXIS = 3


def test(txtPath, model, label, sequen):  # 檔案路徑，.h5檔案，手勢的正確分類
    sample = []

    # 將 data 逐行儲存於 sample 
    with open(txtPath) as test_case:
        for line in test_case:
            s = line.strip().split(',')
            try:
                sample.append(list(map(float, s[0:3])))  
            except:
                pass

    # sample = [sample[0]*31] + sample + [sample[-1]*30]
    sample = [sample[0]] * int((WSIZE / 2 + 0.5)) + sample + [sample[-1]] * int((WSIZE / 2))

    samples = []
    # 前處理: 使用 Sliding Window 在 sample 上逐一滑動，產生多個 window 儲存於 samples.
    for i in range(len(sample) - WSIZE + 1):
        samples.append(sample[i:i + WSIZE])

    # rawResult=模型 softmax 結果
    rawResult = model.predict(np.array(samples).reshape(len(samples), WSIZE, AXIS))

    # maxResult=rawResult 的 softmax 結果中最大者
    maxResult = []
    for i in rawResult:
        maxResult.append(i.argmax())
    # print(maxResult)


    sequen.orderPredict(maxResult, label)

##########################
###        main        ###
##########################
print("Begin")

confArray = np.empty(MODELNUM, dtype=list)
allAccuracy = np.empty(MODELNUM, dtype=float)

for countTime in range(MODELNUM):
    gesCount = 0
    modelName = 'model/' + MODELPATH + '/' + str(countTime + 1) + '_' + MODELPATH + '.h5'
    model = load_model(modelName)

    ordAcc = OrderAccuracy()

    print('\n')
    print('Model-', countTime + 1, ': ')
    for label in listdir(TESTPATH):
        subdir = path.join(TESTPATH, label)

        ordAcc.newline = 0  # 開始不同類別時將 歸零

        for srcTxt in listdir(subdir):
            # Ignore un-relavent files
            if '.txt' not in srcTxt:
                continue

            txtPath = path.join(subdir, srcTxt)

            # l 中存放手勢的分類 例如：test\test3\1-2\SensorData_2017_11_21_161824，則 l = [1,2]
            l = list(map(int, label.split('-')))
            test(txtPath, model, l, ordAcc)  # 檔案路徑，modle，手勢的正確分類，ordAcc
            # ordAcc.printAns()
    ordAcc.printConfuseArray()
    ordAcc.printGesBup()
