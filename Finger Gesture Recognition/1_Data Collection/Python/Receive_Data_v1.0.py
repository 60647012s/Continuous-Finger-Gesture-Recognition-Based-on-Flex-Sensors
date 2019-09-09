import serial  
import struct  
import numpy  
import os  
import time 
import msvcrt  

############################################
###      設定檔案路徑、使用者以及手勢       ###
############################################

PATH = 'Sensor_Data/trainData/'  # 接收檔案儲存路徑
USER = "W.C_Chuang"  # 資料蒐集者
DATE = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 當天日期
GESTURE = "1"  # 手勢動作
DATASET = "TR"  # 手勢資料集: "TR=轉接手試"
# SERIAL = serial.Serial('COM9', 9600, timeout=2)  # 與連接端口建立連線 ('連接埠', 'BAUD')
SERIAL = serial.Serial('COM3', 115200, timeout=2)


# 鍵按鍵監聽
def hit_key():
    if (msvcrt.kbhit()):  # 若偵測到鍵盤事件
        if (ord(msvcrt.getch()) == 32):  # 若鍵盤事件為 空白建 = 32
            return 1
    return 0


if __name__ == '__main__':

    if not os.path.exists(str(PATH) + str(USER) + '/' + str(DATE) + '-' + str(DATASET) + '/' + str(GESTURE)):
        os.makedirs(str(PATH) + str(USER) + '/' + str(DATE) + '-' + str(DATASET) + '/' + str(GESTURE))  # 產生檔案儲存路徑

    deTime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))  # deTime = 當前詳細時間
    sensor_File = open(str(PATH) + str(USER) + '/' + str(DATE) + '-' + str(DATASET) + '/' + str(GESTURE) + '/' + str(GESTURE) + '_' + str(
        deTime) + '_' + str(USER) + '_' + str(DATASET) + '.txt', 'w')  # 回傳值寫入的文本名稱

    split_F1 = numpy.empty(2, dtype=int)  
    split_F2 = numpy.empty(2, dtype=int)  
    split_F3 = numpy.empty(2, dtype=int)  

    while (1):

        # 等待開始
        while (hit_key() - 1):  
            SERIAL.flushInput()  # 清空 Comport's receive Buffer
            print('waiting')


        # 開始紀錄回傳的感測值
        while (hit_key() - 1):
            check = SERIAL.read().decode("ISO-8859-1") 
            if check == 'S':
 
                split_F1[0] = int(ord(SERIAL.read().decode("ISO-8859-1"))) 
                split_F1[1] = int(ord(SERIAL.read().decode("ISO-8859-1")))
                split_F2[0] = int(ord(SERIAL.read().decode("ISO-8859-1")))
                split_F2[1] = int(ord(SERIAL.read().decode("ISO-8859-1")))
                split_F3[0] = int(ord(SERIAL.read().decode("ISO-8859-1")))
                split_F3[1] = int(ord(SERIAL.read().decode("ISO-8859-1")))

                full_F1 = (split_F1[0] | split_F1[1] << 8)  
                full_F2 = (split_F2[0] | split_F2[1] << 8)  
                full_F3 = (split_F3[0] | split_F3[1] << 8)  

                full_F1 = struct.pack('i', full_F1)  
                (full_F1,) = struct.unpack('i', full_F1)
                full_F2 = struct.pack('i', full_F2)
                (full_F2,) = struct.unpack('i', full_F2)
                full_F3 = struct.pack('i', full_F3)
                (full_F3,) = struct.unpack('i', full_F3)

                sensor_File.write("%d," % full_F1)
                sensor_File.write("%d," % full_F2)
                sensor_File.write("%d,\n" % full_F3)

                # 寫入結果預覽
                print(full_F1, full_F2, full_F3)

        
        sensor_File.close()  # 關閉文本
        deTime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        sensor_File = open(str(PATH) + str(USER) + '/' + str(DATE) + '-' + str(DATASET) + '/' + str(GESTURE) + '/' + str(GESTURE) + '_' + str(deTime) + '_' + str(USER) + '_' + str(DATASET) + '.txt', 'w')
        SERIAL.flushInput() 
