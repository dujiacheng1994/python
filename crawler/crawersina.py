from bs4 import BeautifulSoup
import requests

total = 0
h = {
    "user-agent": "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"  # 模拟用户访问
}
dir_url = "https://china.huanqiu.com/gangao"
res = requests.get(dir_url, headers=h)
t = res.text

dir = BeautifulSoup(t, "html.parser")  # 解析返回的绘本目录页response
dir_item = dir.find_all('h4')
dir_item = dir.find_all('div', attrs={"class": "con-txt"})


