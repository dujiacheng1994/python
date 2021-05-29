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
picbooks = []
for item in range(len(dir_item)):
    picbooks.append(dir_item[item]['href'])
    try:
        res = requests.get(picbooks[item], headers=h)
        t = res.text
        content = BeautifulSoup(t, "html.parser")  # 解析返回的绘本内容页response
        tmp1 = content.find_all('div', attrs={"class", "work-show-box"})
        tmp2 = tmp1[0].find_all('img')
        image_urls = []  # 存放本绘本图片url
        for unit in tmp2:
            image_urls.append(unit['src'])

        # 下载图片组
        for i in range(len(image_urls)):
            # 创建存储目录
            dir_num = str(item) #todo:目录需要适应多页情况，建立多层目录？
            if not os.path.exists(dir_num):
                os.mkdir(dir_num)
                print("已创建%s" % dir_num)
            # 下载图片存放到对应目录
            try:
                pic = requests.get(image_urls[i], headers=h)
                with open(dir_num + '/' + str(i) + '.jpg', 'wb') as fp:  # todo:格式是否能自动适应？
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


