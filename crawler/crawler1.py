from bs4 import BeautifulSoup
import os
import requests
h = {
    "user-agent":"Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"   #模拟用户访问
}
page=3 #todo:做成遍历所有页面

dir_url="https://www.zcool.com.cn/search/content?type=0&field=0&other=0&sort=5&word=%E7%BB%98%E6%9C%AC&recommend=0&time=0&requestId=requestId_1560846137906&p="+str(i)+"#tab_anchor"
res = requests.get(dir_url,headers = h)
t = res.text

soup = BeautifulSoup(t,"html.parser")   #解析返回的response

dir_item = soup.find_all('a',attrs ={"class":"card-img-hover"})
children=[]
for i in range(len(dir_item)):
   children.append(dir_item[i]['href'])
item_image = soup.find_all('img') #todo:此处图片下载没有必要，要改成跳入所在网址

#创建存储目录
dir_num=str(page)
if not os.path.exists(dir_num):
    os.mkdir(dir_num)
#下载图片
image=[]
for i in range(len(item_image)):
   image.append(item_image[i]['src'])
   try:
      pic = requests.get(image[i], headers=h)
      with open(dir_num+'/'+str(i)+'.png','wb') as fp:
         fp.write(pic.content)
         fp.close()
   except Exception as e:
      print(e)
      continue


# for item in dir_item[2].children:
#     print(item)