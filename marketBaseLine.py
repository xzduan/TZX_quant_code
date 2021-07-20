
"""
 ZFT
 duanxz
 20210713 16:22
"""

import numpy as np
import pandas as pd
import os
from WindPy import w
import json

# 主要目的是获取历史上的指数数据，为了之后进行回测时有可比对象

# 目标目录：marketBaseLine
aim_path = "..\\marketBaseLine"


# 返回数据格式为WindPy.w.WindData，{.ErrorCode,.Codes,.Fields,.Times,.Data}

indexList = {
"NH0100.NHF", # 南华商品
"NH0300.NHF", # 南华农产品
"NH0500.NHF", # 南华能化
"NH0600.NHF", # 南华贵金属
"NH0700.NHF", # 南华有色金属
"NH0800.NHF", # 南华黑色
"IF.CFE" # 沪深300


}

'''
w.wsd("NH0100.NHF", "close,volume", "2021-07-06", "2021-07-12", "")
'''


def getData(Wind_code):

    #收盘价格、成交量
    fields = "close,volume";
    beginTime = "2018-01-01 00:00:00";
    endTime = "2021-06-20 00:00:00";
    options = ""
    
    w_wsd_data = w.wsd(Wind_code, fields, beginTime, endTime, options);
    
    
    if w_wsd_data.ErrorCode != 0:
        print("error! ErrorCode is %s" %w_wsd_data.ErrorCode)
        
    return w_wsd_data


# 保存w.wsd()获取的数据
def saveData(Wind_data, save_path):
    if Wind_data.ErrorCode == 0:
        df = pd.DataFrame(Wind_data.Data, index = Wind_data.Fields);
        tempList = [Wind_data.Times];
        df2 =df.append(tempList).rename(index={0:'times'});
        
        df2.to_json(force_ascii = False, path_or_buf = save_path)
    
    return

# 
def runFunc():
    
    w.start();
    
    if os.path.exists(aim_path) == False:
        os.mkdir(aim_path);
    # 循环指数，wsd获取数据
    
    for comJsonIndex in indexList:
        
        savePath = aim_path + '\\' + '%s.json' %comJsonIndex
        
        conTraMinData = getData(comJsonIndex);
        # print(conTraMinData.ErrorCode)
        
        saveData(conTraMinData, savePath);
        
        # 超量判断跳出
        if conTraMinData.ErrorCode == -40522017:
        
            print('w_wsd function is limited. ErrorCode is -40522017.');
            return;
        
    w.stop();


if __name__ == '__main__':
    runFunc();