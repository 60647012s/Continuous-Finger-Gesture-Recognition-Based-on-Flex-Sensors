import os
'''
    目的 : 走訪輸入目錄下的所有文件，並回傳所有文件的絕對路徑
    輸入 : 目標目錄
    輸出 : 目標目錄下所有文件的絕對路徑    
'''
class Folder():
    def __init__(self, targetDir):
        self.targetPath = targetDir  # 目標目錄
        self.totalFilePath = list()  # 目標目錄下所有文件的絕對路徑

    '''
        輸出 : 目標目錄下所有文件的絕對路徑
    '''
    def absTotalFilePath(self):
        # 走訪所有目標目錄下的文件, 回傳文件名稱與路徑資訊
        for dirPath, dirNames, fileNames in os.walk(self.targetPath):  # __, __, __ = 文件父目錄絕對路徑, 文件上一層目錄名稱, 文件名稱
            # 紀錄所有文件的絕對路徑
            for count_Filename in os.listdir(dirPath):  # 逐一走訪每個文件
                abs_FilePath = dirPath + "/" + count_Filename  # abs_FilePath = 文件的絕對路徑
                # 判斷是否為文件
                if os.path.isfile(abs_FilePath):  # 若 abs_FilePath 是 ".txt"
                    self.totalFilePath.append(abs_FilePath)  # 用 self.totalFilePath 紀錄該文件的絕對路徑
        # print(self.totalFilePath)
        # print(len(self.totalFilePath))
        return self.totalFilePath

if __name__ == '__main__':
    FilePath = Folder("C:/Users/Eric/Desktop/Handover/2_Smart_Glove_System/1_Data Collection/Python/Sensor_Data")
    print(FilePath.absTotalFilePath())