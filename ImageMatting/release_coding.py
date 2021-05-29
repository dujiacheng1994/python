# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pandas as pd

cropped_color = 0
# 加载原始RGB图像
def loadData(backpath,frontpath):
    back = cv2.imdecode(np.fromfile(backpath, dtype=np.uint8), -1)  # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    front = cv2.imdecode(np.fromfile(frontpath, dtype=np.uint8), -1)  # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    #将透明地区统一为黑色
    for i in range(front.shape[0]):
        for j in range(front.shape[1]):
            if front[i][j][3] == 0:
                front[i][j] = 0,0,0,0
    front = front[:,:,:3]  #4通道转3通道
    front_gray=cv2.cvtColor(front,cv2.COLOR_BGR2GRAY)
    return back,front,front_gray


#截取最大特征图(除掉不透明区域)
def getBackCoordinate(front,front_gray):
    c,wfront,hfront = front.shape[::-1]  #[::-1用于反转列表]
    r = 400     #todo: 特征图初始边长，可调
    rmin = 29   #todo:特征图最小边长，可调
    pad = 10    #todo:搜索步长，大步长速度提高，不要大于rmin
    while 1:
        for i in range(0,hfront-r,pad):
            for j in range(0,wfront-r,pad):
                cropped = front_gray[i:i+r, j:j+r]
                if cropped.min() != 0:
                    cropped_color = front[i:i+r, j:j+r]
                    return cropped_color
        r = r - 10
        if r <= rmin:
            print("寻找特征图失败")
            return np.ones(1)

#特征图匹配小图确定相对小图坐标
def matchFront(front,cropped_color):
    cv2.imwrite('front.png',front)
    cv2.imwrite('cropped_color.png',cropped_color)
    threshold = 0.98
    while threshold > 0.9:
        res2 = cv2.matchTemplate(front, cropped_color, cv2.TM_CCOEFF_NORMED)
        loc2 = np.where(res2 >= threshold)
        if loc2[0].size == 0:
            threshold = threshold-0.04
        else:
            #print("小图匹配可信度%.2f" % threshold)
            for pt2 in zip(*loc2[::-1]):
                continue
            return pt2
    print('匹配小图失败')
    return (0, 0)
#特征图匹配大图确定相对大图坐标
def matchBack(back,cropped_color):
    threshold = 0.98
    while threshold > 0.9:
        res = cv2.matchTemplate(back, cropped_color, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if loc[0].size == 0:
            threshold = threshold - 0.04
        else:
            #print("大图匹配可信度%.2f" % threshold)
            for pt in zip(*loc[::-1]):
                continue
            return pt
    print('匹配大图失败')
    return (0,0)
# 计算坐标
def compute_xy(pt,pt2,back,front):
    x_index = pt[0] - pt2[0]
    y_index = pt[1] - pt2[1]
    x_ratio = 100 * x_index/back.shape[1]
    y_ratio = 100 * y_index/back.shape[0]
    #print(x_ratio,y_ratio)
    return x_ratio,y_ratio

def compute_wh(back,front):
    width = 100 * front.shape[1] / back.shape[1]
    height = 100 * front.shape[0] / back.shape[0]
    return width,height

def getindex(backpath,frontpath):
    name = frontpath.split('/')[1] + '_' + frontpath.split('/')[2].split('.')[0]
    print('处理: %s'% frontpath)
    back,front,front_gray = loadData(backpath,frontpath)
    cropped_color = getBackCoordinate(front, front_gray)
    if cropped_color.size == 1:
        return 0,0,compute_wh(back,front)[0],compute_wh(back,front)[1]
    pt2 = matchFront(front, cropped_color)
    if pt2 == (0,0):
        return 0,0,compute_wh(back,front)[0],compute_wh(back,front)[1]
    pt = matchBack(back, cropped_color)
    if pt == (0,0):
        return 0,0,compute_wh(back,front)[0],compute_wh(back,front)[1]
    x_index,y_index = compute_xy(pt,pt2,back,front)
    width, height = compute_wh(back,front)
    if x_index<= 0:
        x_index = 0
    if y_index <= 0:
        y_index = 0
    return x_index,y_index,width,height

def typefit(path):
    try:
        f=open("%s.png" % path,"rb")
        f.close()
        return "%s.png" % path
    except Exception as e:
        try:
            f=open("%s.jpg" % path,"rb")
            f.close()
            return "%s.jpg" % path
        except Exception as e:
            print("找不到该文件：%s" % path)
            exit()

def excelWrite(df, path="绘本描述-自动填写.xlsx"):
    writer = pd.ExcelWriter(path)
    pd.DataFrame(df[0]).to_excel(excel_writer=writer, sheet_name='绘本',encoding='utf-8', index=False)
    pd.DataFrame(df[1]).to_excel(excel_writer=writer, sheet_name='page',encoding='utf-8', index=False)
    pd.DataFrame(df[2]).to_excel(excel_writer=writer, sheet_name='角色',encoding='utf-8', index=False)
    pd.DataFrame(df[3]).to_excel(excel_writer=writer, sheet_name='意象',encoding='utf-8', index=False)
    pd.DataFrame(df[4]).to_excel(excel_writer=writer, sheet_name='解释图',encoding='utf-8', index=False)
    pd.DataFrame(df[5]).to_excel(excel_writer=writer, sheet_name='对白',encoding='utf-8', index=False)
    writer.save()
    writer.close()

if __name__ == '__main__':
    backpath = "picbook/page1/1.jpg"
    frontpath = 'picbook/page1/丹粟.png'
    x_index, y_index, width, height = getindex(backpath, frontpath)

    sheet = 0
    df = []
    while sheet < 6:
        df.append(pd.read_excel(r'picbook\图片描述.xlsx', sheet_name=sheet))
        sheet = sheet + 1
    #填写角色坐标
    for i in range(len(df[2])):
        name = df[2].get_values()[i][0]
        page = df[2].get_values()[i][1]
        backpath = typefit("picbook/page%d/%d" % (page,page))
        frontpath = typefit("picbook/page%d/%s" % (page, name))
        x_index, y_index, width, height = getindex(backpath, frontpath)
        df[2].iloc[i,2:7] = ["%.1f%%" % x_index,"%.1f%%"% y_index,'',"%.1f%%" % width,"%.1f%%" % height]
    # 填写意象坐标
    for i in range(len(df[3])):
        name = df[3].get_values()[i][0]
        page = df[3].get_values()[i][6]
        backpath = typefit("picbook/page%d/%d" % (page,page))
        frontpath = typefit("picbook/page%d/%s" % (page, name))
        x_index, y_index, width, height = getindex(backpath, frontpath)
        df[3].iloc[i, 1:6] = ["%.1f%%" % x_index, "%.1f%%" % y_index, '', "%.1f%%" % width, "%.1f%%" % height]
    #填写对话坐标
    for i in range(len(df[5])):
        name = df[5].get_values()[i][0]
        page = df[5].get_values()[i][1]
        backpath = typefit("picbook/page%d/%d" % (page,page))
        frontpath = typefit("picbook/page%d/对白/%s" % (page, name))
        x_index, y_index, width, height = getindex(backpath, frontpath)
        df[5].iloc[i, 2:6] = ["%.1f%%" % x_index, "%.1f%%" % y_index, "%.1f%%" % width, "%.1f%%" % height]
    excelWrite(df)

