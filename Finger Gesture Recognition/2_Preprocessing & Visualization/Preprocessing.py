import os
from LIB.FOLDER import Folder
from LIB.MEDIUMFILTER import MediumFilter

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
    return outputFile


'''
    Preprocess(): 
    目的：感測資料前處理
'''
class Preprocess():
    def __init__(self):
        self.name = "init"

    '''
        float KOData = KOhm(int __, int__):
        目的:將電壓值轉為電阻值
          輸入: 1. 分壓電路的固定電阻, 2. 數位電壓值
          輸出: 電阻值. 分壓電路中 Flex Sensor 的電阻值
    '''
    def KOhm(self, fixohm, ADCVolt):
        self.name = "KOhm"

        KOhmData = fixohm * (1023.0 / float(ADCVolt) - 1.0)  # 將 analog Volt. 轉 Ohm
        KOhmData /= 1000  # K 單位
        KOhmData = round(KOhmData, 4)  # 四捨五入到小數點後第四位

        return KOhmData

if __name__ == "__main__":
    AXIS = 3  # 資料維度, 3 根手指
    FIXOHM = 13325  # 分壓電路的固定電阻 13325 Ohm
    NUMAVG = 7
    Volt2KOhm = Preprocess()  # Volt2KOhm 引入 類別:前處理
    totalTxt = Folder("C:/Users/Eric/Desktop/Handover/2_Smart_Glove_System/1_Data Collection/Python/Sensor_Data")  # totalTxt=目標目錄下所有文件的絕對路徑
    re_inPath = "1_Data Collection/Python/Sensor_Data"
    re_outPath = "2_Preprocessing & Visualization/Preproc_Data"

    # 將目標文件的電壓值轉為電阻值，並儲存於指定位置
    for count_FileNum in totalTxt.absTotalFilePath():  # count_FileNum=單一文件的絕對路徑
        with open(count_FileNum, 'r') as txtFile:  # 讀取文件, 'r'=讀
            raw = txtFile.read()

        outTxt = foldersReplace(count_FileNum, re_inPath, re_outPath)  # 生成目標文件的路徑,回傳寫入文件絕對路徑
        with open(outTxt, 'w') as outputFile:  # 寫入文件, 'w'=寫
            countRawIndex = 1  # 換行旗標
            # 將每一個電壓值轉換為電阻值
            for rawData in raw.split(','):  # 以 ',' 分隔，獲得每一個電壓值. rawData=電壓值
                try:  # 忽略文件最後一行空白
                    KOData = Volt2KOhm.KOhm(FIXOHM, rawData)  # 前處理:電壓轉電阻. KOData=電阻值
                    outputFile.write(str(KOData) + ',')  # 將電阻值寫入文本
                    if countRawIndex % AXIS == 0:  # 控制換行
                        outputFile.write('\n')
                    countRawIndex += 1
                except:
                    pass

        # # 均值濾波
        # midFilter = MediumFilter(NUMAVG, AXIS)
        # midFilter.mdFilter(outTxt)