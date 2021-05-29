import os
import re
path = 'every_year_repo/'

for i in range(1,52):
    f = open(path+str(i)+'.txt',"r",encoding="utf-8")  #打开目录下1.txt-51.txt
    str1 = f.read()
    result = re.findall('....年',str1) #正则表达式，匹配"XXXX年"
    year=result[0] #取第1个匹配结果
    f.close()
    os.rename(path+str(i)+'.txt',path+year+'.txt')   #把i.txt重命名成xxxx年.txt
    os.rename(path + str(i) + 'keywords.txt', path + year + 'keywords.txt')
