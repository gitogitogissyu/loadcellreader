import serial
import time
import threading
import numpy as np
import sys

class roadcellManager:
    
    def __init__(self,COMNUM):       
        self.ser = serial.Serial(COMNUM,230400,timeout=None)
        self.line = ""
        self.getdata_flag = False


    #n秒間のデータを抽出するやつ
    def getdata_for_n_sec(self,getsec):
        startTime = time.time()
        
        self.line =""
        times=0
        self.ser.reset_input_buffer()
        #引数分データをスタックするところ
        while(time.time() - startTime <float(getsec)):
            char = self.ser.read(self.ser.in_waiting).decode('utf-8')#https://riptutorial.com/ja/python/example/20311/%E3%82%B7%E3%83%AA%E3%82%A2%E3%83%AB%E3%83%9D%E3%83%BC%E3%83%88%E3%81%8B%E3%82%89%E3%81%AE%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8A
            #in_waitingを使うと溜まったバッファの中身まで全部読める．
            self.line = self.line + char
            times = times +1
        
        return self.dataprocess()



    def getdata_loop(self):
        while(self.getdata_flag):
            char = self.ser.read(self.ser.in_waiting).decode('utf-8')
            self.line = self.line + char

    def start_getdata(self):
        self.line = ""
        self.ser.reset_input_buffer()
        self.getdata_flag = True
        self.dataloop = threading.Thread(target=self.getdata_loop)
        self.dataloop.start()
        print("loadcell data taken is started!")
    
    def getdata(self):
        return self.dataprocess()

    def getdata_elaseBuffer(self):
        data = self.dataprocess()
        self.line = ""
        return data

    def dataprocess(self):
        #データ処理部
        dataStack = []
        rowdata = self.line.split("\r\n")
        for i in range(len(rowdata)):
            splitdata = rowdata[i].split(",")
            dataStack.append(splitdata)

        dataStack = [i for i in dataStack if len(i) == 4] #4つ要素がないやつは削除（末端or頭の処理）
        dataStack = np.array(dataStack,int)
        return dataStack

    def stop_getdata(self):
        self.getdata_flag = False
        self.dataloop.join()
        print("loadcell data taken is stopped!")

    
    def get_init(self):
        print("start getting initial point...")
        datastack = self.getdata_for_n_sec(1.0)
        print("this is initial point")
        ret_data = datastack.mean(axis=0)
        print(ret_data)

        return ret_data

