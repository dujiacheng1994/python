from bs4 import BeautifulSoup
import os
import requests
total = 0
h = {
    "user-agent": "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"  # 模拟用户访问
}
page = 1  # todo:做成遍历所有页面
dir_url = "https://www.zcool.com.cn/search/content?type=0&field=0&other=0&sort=5&word=%E7%BB%98%E6%9C%AC&recommend=0&time=0&requestId=requestId_1560846137906&p=" + str(
    page) + "#tab_anchor"
res = requests.get(dir_url, headers=h)
t = res.text

dir = BeautifulSoup(t, "html.parser")  # 解析返回的绘本目录页response

dir_item = dir.find_all('a', attrs={"class": "card-img-hover"})
children_urls = []
for item in range(len(dir_item)):
    children_urls.append(dir_item[item]['href'])
    try:
        res = requests.get(children_urls[item], headers=h)
        t = res.text
        content = BeautifulSoup(t, "html.parser")  # 解析返回的绘本内容页response
        images = content.find_all('img', attrs={"class": "lazy-img-class" and "no-right-key"})  # 得到绘本内容图片url组
        # 下载图片组
        image = []
        for i in range(len(images)):
            image.append(images[i]['src'])
            # 创建存储目录
            dir_num = str(item)
            if not os.path.exists(dir_num):
                os.mkdir(dir_num)
                print("已创建%s" % dir_num)
            # 下载图片存放到对应目录
            try:
                pic = requests.get(image[i], headers=h)
                with open(dir_num + '/' + str(i) + '.jpg', 'wb') as fp: #todo:格式是否能自动适应？
                    fp.write(pic.content)
                    fp.close()
                    total = total + 1
                    print(total)
            except Exception as e:
                print(e)
                continue
        print("成功下载第%d绘本" % item)
    except Exception as e:
        print(e)
        continue
