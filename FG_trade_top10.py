
"""
 ZFT
 duanxz
 20210524 17:37
"""

import numpy as np
import pandas as pd
import os
from WindPy import w
import json

# 根源目录：FOF_FG_CTA
ori_path = "..\\FOF_FG_CTA"

# 目标目录：FOF_FG_trade_top10
aim_path = "..\\FOF_FG_trade_top10"


# 根据wind中的商品期货的命名规则，利用.wset.函数获取某合约.空头.多头.交易量.的龙虎榜
# 先从.FOF_FG_CTA.获取所有合约
# 返回数据格式为WindPy.w.WindData，{.ErrorCode,.Codes,.Fields,.Times,.Data}
def getCom():
    return os.listdir(ori_path)


# parameter:查询类型('openinterestranking', 'futurevir')、品种的windcode，合约的windcode，空或者多
# example: getData('openinterestranking' , 'RB.SHF' , 'RB2110.SHF' , 'long')
# 若orderBy为空，则获取数据为交易量查询
def getData(selType, comCode, conCode, orderBy):

    #
    beginTime = "startdate=2015-01-01 00:00:00;";
    endTime = "enddate=2021-05-20 00:00:00;";
    varity = "varity=%s;" %comCode;
    wind_code = "wind_code=%s;" %conCode;
    order_by = "order_by=%s;ranks=all" %orderBy;
    
    if orderBy != '':
        options = beginTime + endTime + varity + wind_code + order_by;
    else:
        options = beginTime + endTime + varity + wind_code + "ranks=all"; 
    # options = 'startdate=2021-02-18;enddate=2021-05-18;varity=RB.SHF;wind_code=RB2110.SHF;order_by=long;ranks=all'
    
    w_wset_data = w.wset(selType, options);
    
    if w_wset_data.ErrorCode != 0:
        print("error! ErrorCode is %s" %w_wset_data.ErrorCode)
        
    return w_wset_data


# 保存w.wset()获取的数据
def saveData(Wind_data, save_path):
    if Wind_data.ErrorCode == 0:
        df = pd.DataFrame(Wind_data.Data, index = Wind_data.Fields)
        df.to_json(force_ascii = False, path_or_buf = save_path)
    
    return

# parameter :selType, orderBy 见getData(); aimType.为'long','short','volume'
def runFunc(selType, orderBy, aimType):
    
    w.start();
    
    aim_path_son = aim_path + '\\' + aimType;
    
    if os.path.exists(aim_path_son) == False:
        os.mkdir(aim_path_son);
        
    # 循环商品，循环某商品的合约，wset获取合约的分钟交易数据
    commodityList = getCom();
    
    for comJsonIndex in commodityList:
       commodityPath = ori_path + '\\' + comJsonIndex;
       
       if os.path.getsize(commodityPath) == 0:
           continue;
       
       with open(commodityPath, 'r') as load_f:
           load_dict = json.load(load_f);

       # 文件目录确认, comAimPath,为某商品的目录，该目录下各合约数据json存储
       comAimPath = aim_path_son + '\\' + comJsonIndex;
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
           
           # (selType, comCode, conCode, orderBy):
           conTraMinData = getData(selType, comJsonIndex, conWindCode, orderBy);
           # print(conTraMinData.ErrorCode)
           saveData(conTraMinData, savePath);
           
           # 超量判断跳出
           if conTraMinData.ErrorCode == -40522017:
           
               print('w_wset function is limited. ErrorCode is -40522017.');
               return;
           
    w.stop();


if __name__ == '__main__':
    runFunc('openinterestranking', 'long','long');
    
    runFunc('openinterestranking', 'short','short');
    
    runFunc('futureoir', '','volume');