
"""
 ZFT
 duanxz
 20210520 19:22
"""

import numpy as np
import pandas as pd
import os
from WindPy import w
import json

# 根源目录：FOF_FG_CTA
ori_path = "..\\FOF_FG_CTA"

# 目标目录：FOF_FG_trade_min
aim_path = "..\\FOF_FG_trade_min"


# 根据wind中的商品期货的命名规则，利用wsi函数获取某合约历史交易数据
# 先从FOF_FG_CTA获取所有合约
# 返回数据格式为WindPy.w.WindData，{.ErrorCode,.Codes,.Fields,.Times,.Data}
def getCom():
    return os.listdir(ori_path)


def getData(Wind_code):

    fields = "open,high,low,close,volume,oi,amt,pct_chg,chg,begin_time";
    beginTime = "2015-01-01 00:00:00";
    endTime = "2021-05-20 00:00:00";
    options = ""
    
    w_wsi_data = w.wsi(Wind_code, fields, beginTime, endTime, options);
    
    
    if w_wsi_data.ErrorCode != 0:
        print("error! ErrorCode is %s" %w_wsi_data.ErrorCode)
        
    return w_wsi_data


# 保存w.wset()获取的数据
def saveData(Wind_data, save_path):
    if Wind_data.ErrorCode == 0:
        df = pd.DataFrame(Wind_data.Data, index = Wind_data.Fields)
        df.to_json(force_ascii = False, path_or_buf = save_path)
    
    return

# 
def runFunc():
    
    w.start();
    
    if os.path.exists(aim_path) == False:
        os.mkdir(aim_path);
    # 循环商品，循环某商品的合约，wsi获取合约的分钟交易数据
    commodityList = getCom();
    
    for comJsonIndex in commodityList:
       commodityPath = ori_path + '\\' + comJsonIndex;
       
       if os.path.getsize(commodityPath) == 0:
           continue;
       
       with open(commodityPath,'r') as load_f:
           load_dict = json.load(load_f);

       # 文件目录确认, comAimPath,为某商品的目录，该目录下各合约数据json存储
       comAimPath = aim_path + '\\' + comJsonIndex;
       comAimPath = comAimPath[:-5];
       
       if os.path.exists(comAimPath) == False:
           os.mkdir(comAimPath);
       
       for conDictIndex in load_dict:
           conWindCode = load_dict[conDictIndex]['wind_code'];
           
           # conWindCode，为某合约的wind代码；savePath，为合约交易数据存为json的相对路径；如存在对应路径的文件则跳过；
           savePath = comAimPath + '\\' + '%s.json' %conWindCode
           
           if os.path.exists(savePath) == True:
               print('the trade_min_data %s is already gotten' %conWindCode)
               continue;
           
           conTraMinData = getData(conWindCode);
           # print(conTraMinData.ErrorCode)
           saveData(conTraMinData, savePath);
           
           # 超量判断跳出
           if conTraMinData.ErrorCode == -40522017:
           
               print('w_wsi function is limited. ErrorCode is -40522017.');
               return;
           
    w.stop();


if __name__ == '__main__':
    runFunc();