import sys
###########################
##   seqence accurate   ###
###########################
CLASSNUM = 4  # 手勢種類



class OrderAccuracy():
    def __init__(self):
        self.classRec = [0] * CLASSNUM  # Recognize 結果累計

        self.confuseArray = [[0] * CLASSNUM for i in range(CLASSNUM)]
        self.allLabelCount = 0
        self.allCorrect = 0
        self.Accuracy = 0

        self.inputLabel=[]
        self.ouputLabel = []
        self.newline = 0

        self.singleLabel = 0.00000000000000001
        self.singleCorrect = 0
        self.twoLabel = 0.00000000000000001
        self.twoCorrect = 0
        self.threeLabel = 0.00000000000000001
        self.threeCorrect = 0

    def orderPredict(self, maxResult, inlabel):    #label 手勢分類，如 "1-2" 則為 [1, 2]; maxResult 為 softmax
        self.inputLabel = inlabel
        nowClass = maxResult[0]    # 目前類別
        conClass = maxResult[0]    # 上一個類別
        seq = [0] * CLASSNUM    # 所有類別 各別的最長連續長度
        Queseq = 0    # "目前類別" 的連續長度
        maxGes = []    # 符合輸入 label 個數的 list
        ending = 0  # EOF 處理

        # 動態建立符合輸入 inlabel 元素個數的 list 。
        for i in range(len(inlabel)):  # 手勢個數
            maxGes.append(i)  # 預設最大手勢由 0 開始.如 inlabel=[0,4], 則建立 maxGes=[0,1] 

        # 找出 len(maxGes) 個，最長連續且不重複的類別
        for index_mC in range(len(maxResult)):
            nowClass = maxResult[index_mC]  # 現在的類別

            if conClass == nowClass and ending == 0:  # 目前類別與上一個類別相同
                Queseq += 1  # 連續次數 +1
                if index_mC == len(maxResult)-2:
                    ending = 1

            elif conClass != nowClass or ending == 1:  #若目前類別與上一個類別不同 或 到達結尾
                minSeq = Queseq
                delSwitch = 0
                # 若 目前類別 已經存在於 maxGes 中
                if conClass in maxGes:
                    if minSeq > seq[conClass]:
                        delete = conClass
                        delSwitch = 1
                
                # 若 目前類別 不存在於 maxGes 中
                elif conClass not in maxGes:
                    for count_Label in range(len(inlabel)):
                        if minSeq > seq[maxGes[count_Label]]:
                            minSeq = seq[maxGes[count_Label]]
                            delete = maxGes[count_Label]
                            delSwitch = 1

                # 若需要替換 maxGes 的類別
                if delSwitch == 1:
                    del maxGes[maxGes.index(delete)]
                    maxGes.append(conClass)
                    seq[conClass] = Queseq

                Queseq = 1
                conClass = nowClass

        self.ouputLabel = maxGes

        # 類別辨識率
        for count_MaxGes in range(len(maxGes)):
            self.classRec[inlabel[count_MaxGes]] += 1  # Recognize 結果累計
            self.confuseArray[inlabel[count_MaxGes]][maxGes[count_MaxGes]] += 1

        # 總體辨識率
        self.allLabelCount += len(inlabel)
        for labelNum in range(len(inlabel)):
            if maxGes[labelNum] == inlabel[labelNum]:
                self.allCorrect += 1

        # 單一手勢,二連續,三連續辨識率
        if len(self.inputLabel) == 1:
            self.singleLabel += len(self.inputLabel)
            for labelNum in range(len(self.inputLabel)):
                if maxGes[labelNum] == self.inputLabel[labelNum]:
                    self.singleCorrect += 1
        if len(self.inputLabel) == 2:
            self.twoLabel += len(self.inputLabel)
            for labelNum in range(len(self.inputLabel)):
                if maxGes[labelNum] == self.inputLabel[labelNum]:
                    self.twoCorrect += 1
        if len(self.inputLabel) == 3:
            self.threeLabel += len(self.inputLabel)
            for labelNum in range(len(self.inputLabel)):
                if maxGes[labelNum] == self.inputLabel[labelNum]:
                    self.threeCorrect += 1

    ###################################
    ###  輸出 {[預測結果][正確結果]}  ###
    ###################################
    def printAns(self):
        if self.newline % 5 == 0:  # 五個一組換行
            print()
        self.newline += 1

        if self.ouputLabel != self.inputLabel:  # 找到錯誤答案上色
            sys.stdout.write("\033[0;31m") # 若辨識錯誤則將輸出改為"紅色"
            print('{', self.ouputLabel, self.inputLabel, '}', end=',  ')
            sys.stdout.write("\033[0;0m")  # 將輸出顏色還原
        else:
            print('{', self.ouputLabel, self.inputLabel, '}', end=',  ')


    ###########################
    ###    confuse array    ###
    ###########################
    def printConfuseArray(self):
        print('\n')
        print('confuse array')

        for row in range(CLASSNUM):
            # print(self.classRec[row])
            for col in range(CLASSNUM):
                if self.classRec[row] != 0:
                    self.confuseArray[row][col] /= self.classRec[row]
                    print("%.4f" % float(self.confuseArray[row][col]), end="  ")
                else:
                    print("%.4f" % float(self.confuseArray[row][col]), end="  ")
            print("\n")


        self.Accuracy = (1. * self.allCorrect) / (1. * self.allLabelCount)
        print('Overall')
        print(self.allCorrect, '/', self.allLabelCount, '=')
        print(self.Accuracy)

    '''
    '''
    def printGesBup(self):
        print('\n')
        print("Single:", self.singleCorrect / self.singleLabel)
        print("Two:", self.twoCorrect / self.twoLabel)
        print("Three:", self.threeCorrect / self.threeLabel)




if __name__ == "__main__":
    ans = OrderAccuracy()
    s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    label = [0, 1]
    ans.orderPredict(s, label)
    ans.printAns()
    ans.printConfuseArray()
    ans.printGesBup()