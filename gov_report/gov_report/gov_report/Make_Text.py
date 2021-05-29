#此程序需要安装requests，bs4，re库
import requests
from bs4 import BeautifulSoup
import bs4
import re

def getHTMLText(url):
    """
    获取网页的HTML
    政府工作报告首页和某年报告页面均调用此函数
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getHrefs(html):
    """
    获取政府工作报告首页的链接并生成列表
    修改正则表达式获取不同年份报告的链接
    """
    soup = BeautifulSoup(html,"html.parser")
    hrefs = []
    #获取text包含年份的所有标签a
    a = soup.find_all("a", text = re.compile('(2009)|(201[0-9])'))
    for i in a:
        try:
            href = i.attrs["href"].strip('\r\n')
            hrefs.append(href)
        except:
            continue
    return hrefs

def getPList(html):
    """
    获取某年报告内容的集合
    过滤掉报告内容为空的标签
    """
    soup = BeautifulSoup(html,"html.parser")
    ps = soup.find_all("p")
    plist = []
    for p in ps:
        if p.text != "":
            plist.append(p)
        else:
            pass
    return plist

def getPFile(pfile,plist):
    """
    将报告内容添加至文件
    """
    try:
        with open(pfile, "a", encoding="utf-8") as f:
            for p in plist:
                #去除每一段内容的缩进
                p = ''.join(p.text.split())
                f.write(p+ "\n")
    except:
        return ""

def main():
    """
    主函数流程如下：
    首先从政府工作报告首页爬取数年报告的url链接
    再遍历url链接，爬取每年的报告内容并写入文件
    """
    url = "http://www.gov.cn/guowuyuan/baogao.htm"
    html = getHTMLText(url)
    hrefs = getHrefs(html)
    for href in hrefs:
        href_html = getHTMLText(href)
        plist = getPList(href_html)
        output_file = "Desktop/gov_report/Text/2009_2019.txt"
        getPFile(output_file,plist)
        
if __name__ == '__main__':
    main()

