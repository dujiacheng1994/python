#coding:utf-8
import requests
import pandas as pd
h = {
    "user-agent":"Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"   #模拟用户访问
}
mylist = []
for num in range(10000,20000):   #这里设置人物信息范围
    try:
        #获取数据
        if num%100 == 0: print(num)
        dir_url="http://ldzl.people.com.cn/dfzlk/front/personPage"+ str(num) + ".htm"
        res = requests.get(dir_url,headers = h)
        if res.status_code == 404: continue
        t = res.text
        mylist.append(t)
    except Exception as e:
        print(str(num)+':')
        print(e)
        continue
df = pd.DataFrame(data=mylist)
df.to_csv("./10000-20000.csv", encoding="utf-8-sig", mode="a", header=False, index=False)