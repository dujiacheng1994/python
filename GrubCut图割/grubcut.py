import numpy as np
import cv2
from matplotlib import pyplot as plt
import warnings

warnings.filterwarnings("ignore", module="matplotlib")

imgpath = "2.png"
img = cv2.imread(imgpath)

Coords1x, Coords1y = 'NA', 'NA'
Coords2x, Coords2y = 'NA', 'NA'


def OnClick(event):
    # 获取当鼠标"按下"的时候，鼠标的位置
    global Coords1x, Coords1y
    if event.button == 1:
        try:
            Coords1x = int(event.xdata)
            Coords1y = int(event.ydata)
        except:
            Coords1x = event.xdata
            Coords1y = event.ydata
        print("#### 左上角坐标 ：", Coords1x, Coords1y)


def OnMouseMotion(event):
    # 获取当鼠标"移动"的时候，鼠标的位置
    global Coords2x, Coords2y
    if event.button == 3:
        try:
            Coords2x = int(event.xdata)
            Coords2y = int(event.ydata)
        except:
            Coords2x = event.xdata
            Coords2y = event.ydata
        print("#### 右下角坐标 ：", Coords2x, Coords2x)


def OnMouseRelease(event):
    if event.button == 2:
        fig = plt.gca()
        img = cv2.imread(imgpath)
        # 创建一个与所加载图像同形状的Mask
        mask = np.zeros(img.shape[:2], np.uint8)
        # 算法内部使用的数组,你必须创建两个np.float64 类型的0数组,大小是(1, 65)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        # 计算人工前景的矩形区域(rect.x,rect.y,rect.width,rect.height)
        if (Coords2x - Coords1x) > 0 and (Coords2y - Coords1y) > 0:
            try:
                rect = (Coords1x, Coords1y, Coords2x - Coords1x, Coords2y - Coords1y)
                print('#### 分割区域：', rect)
                print('#### 等会儿 有点慢 ...')
                iterCount = 10
                cv2.grabCut(img, mask, rect, bgdModel, fgdModel, iterCount, cv2.GC_INIT_WITH_RECT)
                mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
                img = img * mask2[:, :, np.newaxis]
                plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                plt.subplot(122), plt.imshow(cv2.cvtColor(cv2.imread(imgpath), cv2.COLOR_BGR2RGB))
                fig.figure.canvas.draw()
                print('May the force be with me!')
            except:
                print('#### 先左键 后右键')
        else:
            print('#### 左下角坐标值必须大于右上角坐标')


# 预先绘制图片
fig = plt.figure()
plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.subplot(122), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.colorbar()

# 鼠标左键，选取分割区域（长方形）的左上角点
fig.canvas.mpl_connect('button_press_event', OnClick)
# 鼠标右键，选取分割区域（长方形）的右下角点
fig.canvas.mpl_connect('button_press_event', OnMouseMotion)
# 鼠标中键，在所选区域执行分割操作
fig.canvas.mpl_connect('button_press_event', OnMouseRelease)
plt.show()

# 连接鼠标点击事件
# fig.canvas.mpl_connect('motion_notify_event', OnMouseMotion)
# 连接鼠标移动事件
# fig.canvas.mpl_connect('button_release_event', OnMouseRelease)
# plt.show()
