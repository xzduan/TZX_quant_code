
"""
 ZFT
 duanxz
 20210524 17:05
"""

import numpy as np
import pandas as pd
import os
from WindPy import w


# 目标目录：FOF_FG_cash
aim_path = "..\\FOF_FG_cash"

# 已选取的大宗商品（26）对应的现货代码
'''
#### 能源（1）

* 动力煤	ZC.CZC

  S5120089

  动力煤现货山西产秦皇岛港市场价 Q5500

#### 农产品（7）

* 豆1（区别于豆2，国内产且为非转基因，成交量大，价格高）A.DCE

  S5005861,S5005855,S5006390,S5005856,S5005864

  国产三等大连，进口二等青岛、进口广东、国产二等济南、国产三等哈尔滨

* 豆油 Y.DCE

  S5006403,S5006404,S5005994

  豆油国产豆天津，豆油进口豆天津、四级豆油江苏张家港

* 豆粕 M.DCE

  S5006046,S5028831,S5028850,S5082268,S5082277

  豆粕张家港，普通蛋白豆粕山东日照，普通蛋白豆粕山东龙口，普通蛋白豆粕福建福州

* 生猪 LH.DCE

  S5070874,S5070872,S5029017,S5029019

  生猪河南开封，生猪山东临沂，生猪辽宁，生猪四川

* 玉米 C.DCE

  S5028929,S5006519,S5006534,S5006537

  玉米大连平仓价，玉米锦州港，玉米大连港，玉米鲅鱼圈

* 棉花 CF.CZC

  S5005957,S6941491,S6941493,S6941494

  棉花新疆、棉花新疆1129B，棉花新疆3128B，棉花新疆4128B

* 菜粕 RM.CZC

  S5005872,S5005882,S5041871

  菜粕现货黄埔，菜粕现货沈阳、菜粕现货福建

#### 黑色（6）

* 铁矿	I.DCE

  S0174655,S0265483

  青岛港PB粉矿61.5%、青岛港金布巴粉61%

* 焦煤	 JM.DCE

  S5120097,S5112232

  主焦煤吕梁产（A\<10.5；V:20-24%;S\<1%,G\>75%）、主焦煤京唐港库提价澳大利亚产（A:9%,V26%,0.4%S,G87,Y15mm）

* 焦炭 J.DCE

  S0033507,S5118429,S5120133

  二级冶金焦（A13.5%，.7%S）唐山出厂价、天津港平仓价准一级冶金焦、连云港平仓价一级冶金焦（反应性27）

* 螺纹钢 RB.SHF

  S0033227,S0073207,S5704770,S5707139

  上海20mm、hangzhou 20mm、天津20mm、上海12mm

* 线材 WR.SHF

  S0033334

  高线6.5HPB235上海

* 热轧卷板 HC.SHF

  S0033272,S0073208,S0033240,S0033249

  上海4.75mm、天津3.0mm、广州3.0mm、上海3.0mm

#### 化工（5）

* PTA TA.CZC

  S5439947,S5435640

  市场中间价PTA现货华东、CCFEI价格指数PTA内盘

* 乙二醇 EG.DCE

  S5439184,S5439173,S5439176,S5439178

  乙二醇现货华东中间价、乙二醇现货华南低端价、乙二醇现货东北低端价、乙二醇现货华南高端价

* 甲醇 MA.CZC

  S5422062,S5418787,S5416981

  甲醇华东地区市场中间价、市场价甲醇江苏、出厂价甲醇山东联盟

* 纯碱 SA.CZC

  S5442125,S5438613,S5470435

  市场平均价重质纯碱华东地区、市场中间价重质纯碱全国、市场价纯碱轻质国内

  > 最后一个存在时间延迟，几天

* 橡胶 RU.SHF

  S5016816,S5470428,S5470429

  市场价天然橡胶云南国营全乳胶SCRWF上海、现货价天然橡胶标准胶1#国内、现货价天然橡胶标准胶3L国内

  > 最后一个存在巨量延迟，几个月

#### 有色（5）

* 铜 CU.SHF

  S0182161,S5806983

  长江有色市场平均价铜1#、上海物贸平均价铜

* 铝 AL.SHF

  S0182162,S5806985

  长江有色市场平均价铝A00、上海物贸平均价铝

* 镍 NI.SHF

  S0105517,S5806989

  平均价镍1#、上海物贸平均价镍

  > 不知道为什么镍品种里有两个基差，而且差距很大。不知道大的那个怎么算出来的

* 金 AU.SHF

  S0202645,S0206705,S0035819

  金交所黄金现货结算价、金交所黄金现货mAu收盘价、金交所黄金现货Au9999收盘价

  > 金交所的黄金的现价和基差都是实时的，这里只能用前一日结算和收盘价进行记录

* 银 AG.SHF

  'S5807139,S0202646

  金交所白银结算价、上海华通结算平均价白银一号国标国产

  > 金交所的白银的现价和基差都是实时的，这里只能用前一日结算和收盘价进行记录

#### 非金属建材（2）

* PVC V.DCE

  S5438385,S5438384,S5438386

  市场中间价PVC电石法华东、市场中间价PVC电石法华北、市场中间价PVC电石法华南

* 玻璃 FG.CZC

  S5914402,S5914198,S5914210,S5914222

  现货价浮法玻璃5mm沙河市安全实业有限公司、现货平均价浮法玻璃5mm北京、现货平均价浮法玻璃5mm上海、现货平均价浮法玻璃5mm广州
'''


# 全体关注品种的核心现货对象
cash_list = {
"S5120089",
"S5005861",
"S5005855",
"S5006390",
"S5005856",
"S5005864",
"S5006403",
"S5006404",
"S5005994",
"S5006046",
"S5028831",
"S5028850",
"S5082268",
"S5082277",
"S5070874",
"S5070872",
"S5029017",
"S5029019",
"S5028929",
"S5006519",
"S5006534",
"S5006537",
"S5005957",
"S6941491",
"S6941493",
"S6941494",
"S5005872",
"S5005882",
"S5041871",
"S0174655",
"S0265483",
"S5120097",
"S5112232",
"S0033507",
"S5118429",
"S5120133",
"S0033227",
"S0073207",
"S5704770",
"S5707139",
"S0033334",
"S0033272",
"S0073208",
"S0033240",
"S0033249",
"S5439947",
"S5435640",
"S5439184",
"S5439173",
"S5439176",
"S5439178",
"S5422062",
"S5418787",
"S5416981",
"S5442125",
"S5438613",
"S5470435",
"S5016816",
"S5470428",
"S5470429",
"S0182161",
"S5806983",
"S0182162",
"S5806985",
"S0105517",
"S5806989",
"S0202645",
"S0206705",
"S0035819",
"S5807139",
"S0202646",
"S5438385",
"S5438384",
"S5438386",
"S5914402",
"S5914198",
"S5914210",
"S5914222"
}



# 根据wind中的商品期货的命名规则，利用edb函数获取某个品种的所有合约
# 返回数据格式为WindPy.w.WindData，{.ErrorCode,.Codes,.Fields,.Times,.Data}
def getData(Wind_code):
    
    beginTime = "2015-01-01 00:00:00";
    endTime = "2021-05-20 00:00:00";
    options = "";
    
    w_edb_data = w.edb(Wind_code, beginTime, endTime, options);
    
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
    
    # 遍历目标现货列表，获取现货价格信息
    for CTA_code in cash_list:
        sec_data = getData(CTA_code)
        saveData(sec_data, CTA_code)

        # 超量判断跳出
        if sec_data.ErrorCode == -40522017:
            print('w_edb function is limited. ErrorCode is -40522017.');
            
            return;

    w.stop()



if __name__ == '__main__':
    runFunc();
