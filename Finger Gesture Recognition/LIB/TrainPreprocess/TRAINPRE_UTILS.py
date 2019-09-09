from os import listdir
import numpy as np
import os
import time as time


'''
    list __ = get_files(str __):
    目的:輸入"資料集"目錄，返回文件路徑與Label
    輸入:資料集目錄
    輸出:(文件路徑,Label) 
'''
def getFiles(path):
    accomplish_path = []
    for subdir in listdir(path):
        for i in listdir(path + '/' + subdir):
            accomplish_path.append((path + '/' + subdir + '/' + i, subdir))
            # 格式如：('train1&2_test2/testData2/0/02_2019-01-11-07-51-08_C.Y_Chen.txt', '0')
    return accomplish_path


######################################
###        Process samples         ### 
######################################
def processData(fileName, train, train_label):
    raw = None
    
    with open(fileName[0]) as raw_file:  # fileName[0] 文件路徑
        raw = raw_file.read()
    
    seq = []  # seq=單一文件的所有感測值,以行為單位
    l = []  # l=單一文件的Label,以行為單位(每一行都給一個 label)

    labels = fileName[1]  #  labels fileName[1] 文件的Label

    for rawData in raw.split('\n'):
        try:
            l.append(int(labels))
            seq.append(list(map(float, rawData.split(',')[0:3])))
            # print(i.split(',')[0:3])
        except:
            pass


    train.append(list(seq))
    train_label.append(list(l[1:]))  # l[1:] ← 為了與 seq 保持相同個數
    return train, train_label


########################################################
###        Get training  samples                     ### 
########################################################
def getSamples(trainFile):
    train = []
    train_label = []

    for count_trF in trainFile:
        train, train_label = processData(count_trF, train, train_label)

    # train = [[0]*3]*11 + train + [[0]*3]*10  #前後補0

    return train, train_label


if __name__ == '__main__':
    train, _ = getSamples(getFiles('目標檔案絕對路徑'))
