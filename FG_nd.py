
"""
 ZFT
 duanxz
 20210531 14:22
"""

import numpy as np
import pandas as pd
import os
from WindPy import w


# 目标目录：FOF_FG_CTA
aim_path = "..\\FOF_nd"

# 国债查询范围
nd_list = {
'M1008698',  #国债即期收益率：一个月
'M1008699',  #国债即期收益率：三个月
'M1008702',  #国债即期收益率：一年
'M1008704',  #国债即期收益率：三年
'M1008706',  #国债即期收益率：五年
'M1008711'  #国债即期收益率：十年
}



# 根据wind中的国债命名规则，利用edb函数获取国债日更新的即期收益率
# 返回数据格式为WindPy.w.WindData，{.ErrorCode,.Codes,.Fields,.Times,.Data}
def getData(Wind_code):

    beginTime = "2015-01-01 00:00:00";
    endTime = "2021-05-20 00:00:00";
    
    w_edb_data = w.edb(Wind_code, beginTime, endTime)
    
    if w_edb_data.ErrorCode != 0:
        print("error! ErrorCode is %s" %w_edb_data.ErrorCode)
    
    return w_edb_data


# 保存w.edb()获取的数据
def saveData(Wind_data, Wind_code):
    df = pd.DataFrame(Wind_data.Data, index = Wind_data.Fields)
 
    df.to_json(force_ascii = False, path_or_buf = aim_path + '\\' + '%s.json' %Wind_code)
    
    return


def runFunc():
    w.start()
    
    # 文件目录确认
    if os.path.exists(aim_path) == False:
        os.mkdir(aim_path)
    
    # 便利目标商品列表，获取品种的合约信息
    for nd_code in nd_list:
        sec_data = getData(nd_code)
        saveData(sec_data, nd_code)

        # 超量判断跳出
        if sec_data.ErrorCode == -40522017:
            print('w_edb function is limited. ErrorCode is -40522017.');
            
            return;

    w.stop()



if __name__ == '__main__':
    runFunc();
