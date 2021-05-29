import urllib
from urllib import request
import time
from urllib.parse import quote
import string

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

file = open(r'urls.txt','r',encoding='utf-8-sig')
f = open(r'checkresult.txt','w',encoding='utf-8-sig')
lines = file.readlines()
aa = []
for line in lines:
    temp = line.replace('\n', '')
    aa.append(temp)

print('Start checking url：')
i = 0
for a in aa:
    i = i+1
    tempUrl = quote(a, safe=string.printable)
    try:
        request.urlopen(tempUrl)
        print(str(i)+a + ' Ok')
        f.write(str(i)+ a + ' Ok'+ '\n')
    except urllib.error.HTTPError:
        print(str(i)+ a + ' Error')
        f.write(str(i)+ a + ' Error''\n')
    except urllib.error.URLError:
        print(str(i)+ a + ' Error')
        f.write(str(i)+ a + ' Error''\n')
