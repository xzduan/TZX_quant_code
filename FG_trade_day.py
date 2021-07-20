
"""
 ZFT
 duanxz
 20210524 16:45
"""

import numpy as np
import pandas as pd
import os
from WindPy import w
import json

# 根源目录：FOF_FG_CTA
ori_path = "..\\FOF_FG_CTA"

# 目标目录：FOF_FG_trade_min
aim_path = "..\\FOF_FG_trade_day"


# 根据wind中的商品期货的命名规则，利用.wsd.函数获取某合约历史交易数据
# 先从FOF_FG_CTA获取所有合约
# 返回数据格式为WindPy.w.WindData，{.ErrorCode,.Codes,.Fields,.Times,.Data}
def getCom():
    return os.listdir(ori_path)


def getData(Wind_code):

    # 注册仓单、结算价、交易品种
    fields = "open,low,high,close,settle";
    # fields = "open,low,high,close,settle,st_stock"; 从查询结果来看st_stock不是单一合约的注册仓单，是品种所有合约的，导致历史数据大量冗余
    beginTime = "2015-01-01 00:00:00";
    endTime = "2021-05-20 00:00:00";
    options = "Days=Alldays";
    
    w_wsd_data = w.wsd(Wind_code, fields, beginTime, endTime, options);
    
    
    if w_wsd_data.ErrorCode != 0:
        print("error! ErrorCode is %s" %w_wsd_data.ErrorCode)
        
    return w_wsd_data


# 保存w.wsd()获取的数据
def saveData(Wind_data, save_path):
    if Wind_data.ErrorCode == 0:
        df = pd.DataFrame(Wind_data.Data, index = Wind_data.Fields)
        
        # 将时间Times并入Data中
        tempList = [Wind_data.Times]
        df2 =df.append(tempList).rename(index={0:'Times'})
        
        df2.to_json(force_ascii = False, path_or_buf = save_path)
    
    return

# 
def runFunc():
    
    w.start();
    
    if os.path.exists(aim_path) == False:
        os.mkdir(aim_path);
    # 循环商品，循环某商品的合约，wsd获取合约的日期级交易数据
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
           
           # conWindCode.为某合约的wind代码；savePath.为合约交易数据存为json的相对路径；如存在对应路径的文件则跳过；
           savePath = comAimPath + '\\' + '%s.json' %conWindCode
           
           if os.path.exists(savePath) == True:
               print('the trade_daily_data %s is already gotten' %conWindCode)
               continue;
           
           conTraMinData = getData(conWindCode);
           # print(conTraMinData.ErrorCode)
           saveData(conTraMinData, savePath);
           
           # 超量判断跳出
           if conTraMinData.ErrorCode == -40522017:
           
               print('w_wsd function is limited. ErrorCode is -40522017.');
               return;
           
    w.stop();


if __name__ == '__main__':
    runFunc();