data = []
with open(r"D:\U盘1资料\工作\result.txt",'r',encoding='UTF-8') as f:
    i = 0
    try:
        fp = open(r"D:\after.txt",'w',encoding='UTF-8')
        fp.write("4088585 200\n")
        while True:
            a = f.readline()
            i = i+1
            if a:
                 if len(a.split(' ')[0])==2:
                    fp.write(a)
            else:
                 break
        fp.close()
    finally:
        print(i)
        f.close()
