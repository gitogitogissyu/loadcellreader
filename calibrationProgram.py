import serial
import time
import threading
import numpy as np
import sys

ser = serial.Serial("COM6",230400,timeout=None)
line = ""
getdata_flag = False
dataloop = []

#n秒間のデータを抽出するやつ
def getdata_for_n_sec(getsec):
    startTime = time.time()
    
    line =""
    times=0
    ser.reset_input_buffer()
    #引数分データをスタックするところ
    while(time.time() - startTime <float(getsec)):
        char = ser.read(ser.in_waiting).decode('utf-8')#https://riptutorial.com/ja/python/example/20311/%E3%82%B7%E3%83%AA%E3%82%A2%E3%83%AB%E3%83%9D%E3%83%BC%E3%83%88%E3%81%8B%E3%82%89%E3%81%AE%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8A
        #in_waitingを使うと溜まったバッファの中身まで全部読める．
        line = line + char
        times = times +1
    
    dataStack = []
    rowdata = line.split("\r\n")
    for i in range(len(rowdata)):
        splitdata = rowdata[i].split(",")
        dataStack.append(splitdata)

    dataStack = [i for i in dataStack if len(i) == 4] #4つ要素がないやつは削除（末端or頭の処理）
    dataStack = np.array(dataStack,int)
    return dataStack




if __name__ == "__main__":

    args = sys.argv

    if len(args) < 2:
        print("IMPUT Actual WEIGHT")
        sys.exit()
    
    weight =  str(args[1]) 

    input("get initpoints.Press ANY KEY\n")
    dataStack_init = getdata_for_n_sec(1.0)
    print("init point DATA\n")
    print(dataStack_init.mean(axis =0))

    np.savetxt("initDATA_weight_"+weight+".csv",dataStack_init)

    input("get forced point. PRESS ANY KEY AFTER PUT WEIGHT")
    dataStack_forced = getdata_for_n_sec(1.0)
    print("WEIGHT POINT DATA\n")
    print(dataStack_forced.mean(axis=0))

    np.savetxt("FORCED_DATA_weight_"+weight+".csv",dataStack_forced)

    diff = dataStack_forced.mean(axis=0) - dataStack_init.mean(axis=0)
    print("DIFF")
    print(diff)

    np.savetxt("Diff_weight_"+weight+".csv",diff)

    """
    while(time.time() - startTime <1.0):
        bytesToRead = ser.inWaiting()
        line =ser.read().strip().decode('utf-8')
        if len(line)  > 5:
            data = line.split(",")
            dataStack.append(data)
    
    dataStack = np.array(dataStack)
    print(dataStack)
    """



 

        

        
    """
    while(True):
        mappedData = np.array(line.split(","),dtype =np.int)
        print(mappedData)

    sys.exit()
    """
