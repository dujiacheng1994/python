import pandas as pd
data = []
with open(r"C:\Users\Administrator\Downloads\Tencent_AILab_ChineseEmbedding\Tencent_AILab_ChineseEmbedding.txt",'r',encoding='UTF-8') as f:
    try:
        i = 0
        while True:
            a = f.readline()
            i = i+1
            print(i)
            if a:
                data.append(a)
            else:
                break
    finally:
        print(i)
        f.close()
