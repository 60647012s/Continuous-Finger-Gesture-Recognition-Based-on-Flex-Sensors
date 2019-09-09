import os
from shutil import copyfile
from LIB.FOLDER import Folder

DATASET = "/train1&2_test2"
TRAINDATASET_1 = "/trainData1/"
TRAINDATASET_2 = "/trainData2/"
TESTDATASET = "/testData2/"
TARGETCLASS = "TR"  # 載入檔案目標:TR=轉接手勢
srcFile = Folder("C:/Users/Eric/Desktop/Handover/2_Smart_Glove_System/2_Preprocessing & Visualization/Preproc_Data")


for count_FileNum in srcFile.absTotalFilePath():  # count_FileNum=單一文件的絕對路徑
    count_FileNum = count_FileNum.replace('\\', '/')  # 統一目錄分隔符
    if TARGETCLASS not in count_FileNum:  # 忽略不屬於 TARGETCLASS 的文件
        continue

    # 建立 test 資料集
    if "testData" in count_FileNum:
        txtName = count_FileNum.split('/')[-1]  # txtname=手勢類別
        gLabel = count_FileNum.split('/')[-2]  # gLabel=手勢類別
        gLabel = list(map(int, gLabel.split('-')))  # 連續手勢的類別處理
        reLabel = [i - 1 for i in gLabel]  # 手勢類別 -1, 為符合 category 的輸入

        # 重組被 '-' 分開 -1 後, 的連續手勢類別
        gLabel = str(reLabel[0])
        for count_Label in range(1, len(reLabel)):  # 還原 -1 後的連續手勢類別
            gLabel += '-' + str(reLabel[count_Label])  # 手勢類別間加 '-'

        outPath = os.getcwd() + DATASET + TESTDATASET + gLabel  # 寫入文件目錄
        if not os.path.isdir(outPath):
            os.makedirs(outPath)  # 產生文件儲存路徑

        outTxt = outPath + '/' + txtName  # 寫入文件路徑
        copyfile(count_FileNum, outTxt)  # 複製檔案(來源文件, 輸出文件)

    # 建立 train 資料集
    if "trainData" in count_FileNum:
        txtName = count_FileNum.split('/')[-1]  # txtname=手勢類別
        gLabel = count_FileNum.split('/')[-2]  # gLabel=手勢類別
        gLabel = list(map(int, gLabel))  # 手勢的類別處理

        # trainData 1 : 只包含 4 種主要手勢的訓練資料集
        if len(gLabel) == 1:  # Label 中只含有四個主要手勢的手勢文件
            outPath = os.getcwd() + DATASET + TRAINDATASET_1 + str(gLabel[0] - 1)  # 寫入文件目錄
            if not os.path.isdir(outPath):
                os.makedirs(outPath)  # 產生文件儲存路徑

            outTxt = outPath + '/' + txtName  # 寫入文件路徑
            copyfile(count_FileNum, outTxt)  # 複製檔案(來源文件, 輸出文件)

        # trainData 2 : 包含 4 trainData 1 , 並加入 "轉接手勢"
        outPath = os.getcwd() + DATASET + TRAINDATASET_2 + str(gLabel[0] - 1)  # 寫入文件目錄
        if not os.path.isdir(outPath):
            os.makedirs(outPath)  # 產生文件儲存路徑

        outTxt = outPath + '/' + txtName  # 寫入文件路徑
        copyfile(count_FileNum, outTxt)  # 複製檔案(來源文件, 輸出文件)