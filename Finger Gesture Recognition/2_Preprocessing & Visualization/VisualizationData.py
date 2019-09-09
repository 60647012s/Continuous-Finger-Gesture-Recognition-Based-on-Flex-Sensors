import matplotlib.pyplot as plt
import os
from LIB.FOLDER import Folder

RESET = 1  # 是否重新產生所有波形圖， =1 重新產生, =0 只針對新加入的手勢資料
AXIS = 3  # 3 根手指
totalTxt = Folder("C:/Users/Eric/Desktop/Handover/2_Smart_Glove_System/2_Preprocessing & Visualization/Preproc_Data")  # totalTxt=目標目錄下所有文件的絕對路徑
re_inPath = "Preproc_Data"
re_outPath = "Visualiztion"


def addFolder(path):
    if not os.path.isdir(path):
        os.makedirs(path)

'''
    str outputTXT = foldersReplace(str __, str__, str__):
    目的：產生寫入目標的目錄
      輸入：1. 來源文件絕對路徑, 2. 來源文件路徑要被取代的部分, 3. 寫入文件取代後的路徑名稱
            來源路徑為 "a/b/c/d"
            寫入路徑為 "a/f/c/d"
            則來源       1. 為  "a/b/c/d"
            來源取代部分  2. 為  "b"
            寫入取代名稱  3. 為  "f"

      輸出：寫入文件絕對路徑
'''
def foldersReplace(srcFile, re_srcPath, re_outputPath):
    tempsrcFile = srcFile
    tempsrcPath = os.path.dirname(srcFile)
    outputPath = tempsrcPath.replace(re_srcPath, re_outputPath)
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)  # 產生文件儲存路徑

    outputFile = tempsrcFile.replace(re_srcPath, re_outputPath)
    outputFile = outputFile.replace('.txt', '.png')  # .txt 改 .PNG
    return outputFile


# yLabel_最大最小值
MaxData = 0.0
MinData = 65535
for count_FileNum in totalTxt.absTotalFilePath():
    with open(count_FileNum) as txtFile:
        raw = txtFile.read()

    for count_rawData in raw.split(','):
        try:
            if float(count_rawData) > float(MaxData):
                MaxData = float(count_rawData)
                maxFile = count_FileNum
            if float(count_rawData) < float(MinData):
                MinData = float(count_rawData)
                minFile = count_FileNum
        except:
            pass

# print(maxFile)
print("MaxData:", MaxData)
# print(minFile)
print("MinData:", MinData)



# 讀取文本並畫圖
for count_FileNum in totalTxt.absTotalFilePath():
    outPNG = foldersReplace(count_FileNum, re_inPath, re_outPath)
    print(outPNG)


    #  跳過已視覺化的檔案
    if RESET == 0:  # 是否將全部資料重新產生波形圖
        if os.path.isfile(outPNG):  # 若已存在
            print("Exist")
            continue

    # 讀取文本
    with open(count_FileNum) as txtFile:
        raw = txtFile.read()

    # 動態宣告 Fingers_X, 由零開始
    for index_AXIS in range(AXIS):
        locals()["Fingers_%s" % str(index_AXIS)] = []

    dataNum = 0
    for count_rawData in raw.split('\n'):
        try:
            for index_AXIS in range(AXIS):
                locals()["Fingers_%s" % str(index_AXIS)].append(float(count_rawData.split(',')[index_AXIS]))
            dataNum += 1
        except:
            continue


    plt.clf()
    plt.figure(0)  # figsize(寬, 高) (圖片大小)

    plt.subplots_adjust(wspace=20, hspace=0.5)
    # 繪點與label，尚未想好怎麼修(放置)
    plt.plot(locals()["Fingers_%s" % str(0)], color='r', label='Thumb')
    plt.plot(locals()["Fingers_%s" % str(1)], color='b', label='Index Finger')
    plt.plot(locals()["Fingers_%s" % str(2)], color='y', label='Middle Finger')

    plt.legend(loc=1, fontsize=14)

    plt.ylabel('KOhm', fontsize=16)  # Y label 由路徑後面數回來第五個

    plt.xlabel('Sample Number', fontsize=16)
    plt.xticks(fontsize=14)  # xlim 字體大小
    plt.yticks(fontsize=14)  # ylim 字體大小
    plt.xlim(0, dataNum, 1)

    # y 軸的最大最小值依上面搜尋結果
    plt.ylim(MinData, MaxData)

    plt.tight_layout(pad=0.1)  # 邊框留白 =0.1 (最小) , 須放在最後(有順序性)
    plt.savefig(outPNG)
    # plt.close()

