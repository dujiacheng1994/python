#coding:utf-8
from bs4 import BeautifulSoup
import re
import pandas as pd
import reference as r
def readRefData(uri):  #读相关等级参考表格
    df = pd.read_excel(uri)
    array = df.values
    dict1 = {}
    for item in array:
        dict1[item[0]] = item[1]
    list1 = list(dict1.keys())
    return dict1,list1
def dataToList(text): #对原始网页格式，按分隔符转化为list
    text = text.replace('\n', '=').replace('\r', '=').replace('\t', '=')
    text = re.sub('[\u3000][\u3000]+', '=', text)
    text = text.replace('\u3000', '').replace(' ', '')
    text = re.sub("[=]+", "=", text)
    text = text.strip('=')
    a = text.split('=')
    b = a[0].split('，') #把第一列一大段个人介绍也分格子
    del(a[0])            #去除原来的大段介绍防止重复
    b=b+a
    return b
def findYear(unit):  #给str,返回开头年份
    # 抛弃格式不为年份开头的奇怪unit
    if len(unit)<=4:
        return -1
    year = unit[0:4]
    if not year.isdigit():
        return -1
    return year
def isContainKey(keylist,text):   #给一个关键词list和一个str，返回是否存在的[0,1,1,0]形式列表
    res = [0]*len(keylist)
    for i in range(len(keylist)):
        if isinstance(keylist[i],list):
            for item in keylist[i]:
                keyword = item
                if text.find(keyword)!=-1:
                    res[i] = 1
                    index = int(text.find(keyword))
                    #print(keyword + text[index:index+10])
        else:
            keyword = keylist[i]
            if text.find(keyword)!=-1:
                res[i] = 1
                index = int(text.find(keyword))
                #print(keyword + text[index:index+10])
    return res
def findLevel(unit): #接受字符串str,返回识别的level
    # 为应对长沙市委书记，市长这种标点分割的情况，要把unit再分割为更小
    unit_list = re.split('，|、', unit)
    level = 0
    test = 0  # 用来控制是否输出关键词用于测试
    for info in unit_list:
        # 先找共青团关键字
        if info.find("团") != -1:
            for key in gongqingtuan_list:
                if (info.find(key) != -1):
                    level = max(level, int(gongqingtuan_dict[key]))
                    break
        # 如果非共青团
        else:
            # 开始识别替换无歧义表
            for key in default_list:
                if info.find(key) != -1:
                    level = max(level, int(default_dict[key]))
                    if test ==1: print(unit + info + key + str(level))
                    break
            # 开始试别具体省市相关级别（多可能表）
            for key in r.changable_level:
                flag = 0 #这是保证在进行特殊市判断后，不会再进行普通市计算
                if info.find(key) != -1:
                    for city in r.zhixiashi:
                        if (unit.find(city)) != -1:
                            level = max(level, int(r.zhixiashi_level[key]))
                            if test == 1: print(unit + info + key + str(level))
                            flag = 1
                            break
                    for city in r.fushengjishi:
                        if (unit.find(city)) != -1:
                            level = max(level, int(r.fushengjishi_level[key]))
                            if test == 1:print(unit + info + key + str(level))
                            flag = 1
                            break
                    for city in r.dijishi:
                        if (unit.find(city)) != -1:
                            level = max(level, int(r.dijishi_level[key]))
                            if test == 1:print(unit+info+key+str(level))
                            flag = 1
                            break
                    if flag == 0:
                        level = max(level, int(r.other_level[key]))
                        if test == 1:print(unit + info + key + str(level))
                        flag = 1
                        break
                if flag == 1: break
    return level
def addWorkplace(placeset,placelist,unit): #接收工作地点set,参考地点list,字符串str
    for place in placelist:
        if unit.find(place) != -1:
            placeset.add(place)

#读官员原始数据
csv_data1 = pd.read_csv("./1-5000.csv")
csv_data2 = pd.read_csv("./5000-10000.csv")
csv_data3 = pd.read_csv("./10000-20000.csv")
csv_data = list(csv_data1.values)+list(csv_data2.values)+list(csv_data3.values)
default_dict, default_list = readRefData("default.xlsx")   #读无歧义表
gongqingtuan_dict, gongqingtuan_list = readRefData("gongqingtuan.xlsx")  #读共青团表

excel_rowslist = [r.header] #初始化要写到excel中的list,先加入标题
#开始工作
for i in range(len(csv_data)):   #遍历excel的每一行
    try:
        row_data = csv_data[i][0]
        soup = BeautifulSoup(row_data,"html.parser")   #解析返回的response
        dir_item = soup.find_all('div',attrs ={"class":"box01"})
        text = dir_item[0].text
        # 获取特征是否存在列表
        features = isContainKey(r.keywordlist_match, row_data)
        currentlevel_text = soup.find_all('i',attrs ={"class":"red"})[0].text
        row_datalist_raw = dataToList(text)
        #识别每一条年份信息
        working_districts = set() #工作地点初始化
        working_shengs = set() #工作省份初始化
        addWorkplace(working_districts,r.diqu,currentlevel_text)
        addWorkplace(working_shengs,r.provinces,currentlevel_text)
        #接下来创造list化为1993=4这种格式
        row_datalist_valid = [row_datalist_raw[0]] #记录有效但存在重复的1999=3这种格式的中间结果
        for i in range(1,len(row_datalist_raw)):
            unit = row_datalist_raw[i] #一个单元格
            year = int(findYear(unit))
            if year==-1: continue
            level = findLevel(unit)
            addWorkplace(working_districts,r.diqu,unit) #筛选城市信息加入
            addWorkplace(working_shengs,r.provinces,unit) #筛选省份信息加入
            if year>0 and level>0:
                row_datalist_valid.append(str(year) + '=' + str(level))
        #接下来创建reformed_row这个list，只留下第一次的年份=等级

        reformed_row = [row_datalist_raw[0]]
        level = 0
        for i in range(1, len(row_datalist_valid)):
            unit = row_datalist_valid[i]
            temp = unit.split('=')        #temp 为[1994,3]这种
            #如果格式正确且标记level大于已填level，则记录该第一次出现level的年份
            if len(temp)<2: continue
            if int(temp[1])>int(level):
                reformed_row.append(unit)
                level = temp[1]
        #开始构建可用来填表的row_toexcel
        row_toexcel = [row_datalist_raw[0], '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(1, len(reformed_row)):
            temp = reformed_row[i].split('=')
            row_toexcel[int(temp[1])] = temp[0]
        #添加工作省份，城市
        row_toexcel.append(findLevel(currentlevel_text))
        row_toexcel.append(','.join(working_shengs))
        row_toexcel.append(','.join(working_districts))
        row_toexcel+=features
    except Exception as e:
        print(str(i)+':')
        print(e)
        continue
    excel_rowslist.append(row_toexcel)

df = pd.DataFrame(data=excel_rowslist)
df.to_csv("./result.csv", encoding="utf-8-sig", mode="a", header=False, index=False)