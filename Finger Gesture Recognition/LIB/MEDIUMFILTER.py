'''
    MediumFilter(int __, int__):
    目的: 將目標文件進行中值濾波，並輸出結果覆蓋目標文件
      輸入:  1. 均值濾波遮罩大小(一次對幾個值進行平均), 2. 手指個數
      輸出: 無
'''
class MediumFilter():
    def __init__(self, numAvg, axis):
        self.numAvg = numAvg  # numAvg=幾個資料取平均
        self.axis = axis  # axis=幾根手指


    '''
        mdFilter(str __):
        目的: 對目標文件進行均值濾波
          輸入: 目標文件絕對路徑
          輸出: 無
    '''
    def mdFilter(self, targetTxt):
        for count_Finger in range(self.axis):  # 依輸入宣告均值濾波矩陣
            locals()["medFil_F_%s" % str(count_Finger)] = [0] * self.numAvg  # locals() 動態宣告變數


        with open(targetTxt, 'r') as txtFile:  # 讀取 targetTxt 文件, 'r+'=可讀寫
            raw = txtFile.read()  # 將文件內儲存於 raw

        # 濾波與寫入
        dataIndCount = 0  # DataIndex=計數目前感測值
        medFilCount = 0  # medFilCount=計數進行濾波的手指
        with open(targetTxt, 'w') as outputFile:  # 寫入文件, 'w'=寫
            for rawData in raw.split(','):  # 令逗號為分隔符
                try:  # 避免結尾空行
                    avgFinger = float(rawData)
                    temprawData = float(rawData)
                    locals()["medFil_F_%s" %
                             str(dataIndCount % self.axis)][medFilCount % self.numAvg] = avgFinger  # 取代濾波器中最舊的值

                    # 判斷當到達第 self.numAvg * self.axis 個感測值後， rawData 開始濾波
                    if dataIndCount >= self.numAvg * self.axis:
                        for count_FilInd in range(self.numAvg):  # 將 self.numAvg 個相加
                            avgFinger += locals()["medFil_F_%s" % str(dataIndCount % self.axis)][count_FilInd]

                        avgFinger = (avgFinger - temprawData) / self.numAvg  # 扣掉自己(rawData)
                        avgFinger = round(avgFinger, 4)  # 四捨五入至小數點第 4 位

                    locals()["medFil_F_%s" %
                             str(dataIndCount % self.axis)][medFilCount % self.numAvg] = avgFinger  # 覆寫均值濾波暫存器中,對應的感測值

                    outputFile.write(str(avgFinger))
                    outputFile.write(',')
                    if dataIndCount % self.axis == (self.axis-1):  # 換行控制
                        outputFile.write('\n')

                    dataIndCount += 1  # DataIndex 計數變數 +1
                    if dataIndCount % self.axis == (self.axis-1):
                        medFilCount += 1  # count_FilInd
                except:  # 結尾空行忽略
                    continue


if __name__ == "__main__":
    test = MediumFilter(7, 3)
    test.mdFilter("目標檔案絕對路徑")
