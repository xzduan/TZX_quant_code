
"""
 ZFT
 duanxz
 20210519 14:22
"""

import numpy as np
import pandas as pd
import os
from WindPy import w


# 目标目录：FOF_FG_CTA
aim_path = "..\\FOF_FG_CTA"

# 已选取的大宗商品（26）
CTA_list = {
# DCE大连商品交易所 # SHF上海期货交易所 # CZC郑州商品交易所
# 能源
"ZC.CZC", # 动力煤 
# 黑色
"I.DCE", # 铁矿
"JM.DCE", # 焦煤
"J.DCE", # 焦炭
"RB.SHF", # 螺纹钢
"WR.SHF", # 线材
"HC.SHF", # 热轧卷板
# 有色
"CU.SHF", # 铜
"AL.SHF", # 铝
"NI.SHF", # 镍
"AU.SHF", # 金
"AG.SHF", # 银
# 非金属建材
"V.DCE", # PVC
"FG.CZC", # 玻璃
# 农品
"A.DCE", # 豆一
"Y.DCE", # 豆油
"M.DCE", # 豆粕
"LH.DCE", # 生猪
"C.DCE", # 玉米
"CF.CZC", # 棉花
"RM.CZC", # 菜粕
# 化工
"TA.CZC", # PTA
"EG.DCE", # 乙二醇
"MA.CZC", # 甲醇
"SA.CZC", # 纯碱
"RU.SHF" # 橡胶
}



# 根据wind中的商品期货的命名规则，利用wset函数获取某个品种的所有合约
# 返回数据格式为WindPy.w.WindData，{.ErrorCode,.Codes,.Fields,.Times,.Data}
def getData(Wind_code):
    option = "startdate=-3Y;wind_code= %s" %Wind_code;
    
    w_wset_data = w.wset('futurecc',option)
    
    if w_wset_data.ErrorCode != 0:
        print("error! ErrorCode is %s" %w_wset_data.ErrorCode)
    
    return w_wset_data


# 保存w.wset()获取的数据
def saveData(Wind_data, Wind_code):
    df = pd.DataFrame(Wind_data.Data, index = Wind_data.Fields)
 
    df.to_json(force_ascii = False, path_or_buf = aim_path + '\\' + '%s.json' %Wind_code)
    
    return




if __name__ == '__main__':
    
    w.start()
    
    # 文件目录确认
    if os.path.exists(aim_path) == False:
        os.mkdir(aim_path)
    
    # 便利目标商品列表，获取品种的合约信息
    for CTA_code in CTA_list:
        sec_data = getData(CTA_code)
        saveData(sec_data, CTA_code)

    w.stop()