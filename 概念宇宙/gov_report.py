import requests
from bs4 import BeautifulSoup
import os
import re

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getURL(url):
    html=getHTMLText(url)
    list=[]
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find_all('a',text=re.compile('(195[4-9])|196[0-9]|197[0-8]'))
    for i in a:
        try:
            hrefs = i.attrs['href'].strip("\r\n")
            if hrefs.startswith("http"):
                list.append(hrefs)
        except:
            continue
    return list

def downLoadContent(text):
    path="before_reform_and_opening_up.txt"
    for i in text:
        with open(path, 'a',encoding='utf-8') as f:
            f.write(i+'\n')

def getReport(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find_all('p')
    content = []
    for i in p:
        if i.text != "":
            content.append(i.text)
        else:
            pass
    print(content)
    return content



def getContent(list):
    for i in list:
        try:
            text = getReport(i)
            downLoadContent(text)
        except:
            continue

def main():
    url='http://www.gov.cn/guowuyuan/baogao.htm'
    list=getURL(url)
    print(list)

    for i in list:
        content = getReport(i)
        print(content)
        downLoadContent(content)


main()