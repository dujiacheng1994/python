import cv2
import numpy as np

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
    threshold = 0.8
    res2 = cv2.matchTemplate(front, cropped_color, cv2.TM_CCOEFF_NORMED)
    loc2 = np.where(res2 >= threshold)
    for pt2 in zip(*loc2[::-1]):
        continue
    return pt2

#特征图匹配大图确定相对大图坐标
def matchBack(back,cropped_color):
    threshold = 0.8
    res = cv2.matchTemplate(back, cropped_color, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        continue
    return pt

# 计算坐标
def compute(pt,pt2,back,front):
    x_index = pt[0] - pt2[0]
    y_index = pt[1] - pt2[1]
    x_ratio = 100 * x_index/back.shape[1]
    y_ratio = 100 * y_index/back.shape[0]
    width = 100 * front.shape[1] / back.shape[1]
    height = 100 * front.shape[0] / back.shape[0]
    return x_ratio,y_ratio,width,height

if __name__ == '__main__':
    backpath = "picbook/page1/1.jpg"
    frontpath = 'picbook/page1/丹粟.png'
    back,front,front_gray = loadData(backpath,frontpath)
    cropped_color = getBackCoordinate(front,front_gray)
    pt2 = matchFront(front, cropped_color)
    pt = matchBack(back,cropped_color)
    x_ratio, y_ratio, width, height = compute(pt,pt2,back,front)




