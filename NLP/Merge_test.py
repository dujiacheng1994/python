import pandas as pd
import numpy as np

left = pd.DataFrame({'key':['a','b','c','d'],
                     'key1':['aa','bb','cc','dd'],
                     'key2':['aaa','bbb','ccc','ddd'],
                     'a':['a0','a1','a2','a3'],
                     'b':['b0','b1','b2','b3']})
right = pd.DataFrame({'key':['a','b','c','d'],
                     'key1':['aa','bb','cc','dd'],
                     'key2':['ko','k0','k0','k0'],
                     'a':['c0','c1','c2','c3'],
                     'b':['d0','d1','d2','d3']})

print(left)
print(right)
res = pd.merge(left.iloc[:,0:2],right.iloc[:,0:2])
print(res)
# res = pd.merge(left,right,on='key1')
# # print(res)
# res2 = pd.merge(left,right,on=['key1','key2'],suffixes=['_k1','_k2'],how='left',indicator=True)
# print(res2)