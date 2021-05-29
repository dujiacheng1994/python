file = r"AIlab.txt"
f = open(file,'r',encoding='UTF-8')
f2=open('result.txt','w',encoding='utf-8')
try:
    i = 0
    while True:
        a = f.readline()
        if a:
            b = a.split()
            if len(b[0])>=4:
                continue
            f2.write(a)
            i = i + 1
        else:
            break

finally:
    print("完成")
    f.close()