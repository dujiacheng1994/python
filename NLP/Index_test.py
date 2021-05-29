import numpy as np
import pandas as pd
#生成随机6x4矩阵
df = pd.DataFrame(np.random.randn(6,4), index=list('abcdef'), columns=list('ABCD'))

#按行整体取
df[:3] #相当于0:2行
df['a':'c'] #从a行到c行
df[[True,True,True,False,False,False]] # 前三行（布尔数组长度等于行数），好处是可以跳着任取
df[df['A']>0] # A列值大于0的行
df[(df['A']>0) | (df['B']>0)] # A列值大于0，或者B列大于0的行
df[(df['A']>0) & (df['C']>0)] # A列值大于0，并且C列大于0的行
#按列整体取
df['A'] #第A列
df[['A','B']]
df[lambda df: df.columns[0]] # 取第0列
#二维索引
df.iloc[3, :]
df.iloc[:3, :] #取前三行
df.iloc[[0,2,4], :]
df.iloc[[True,True,True,False,False,False], :] # 前三行（布尔数组长度等于行数）
df.iloc[df['A']>0, :]       #× 为什么不行呢？想不通！
df.iloc[df.loc[:,'A']>0, :] #×
df.iloc[df.iloc[:,0]>0, :]  #×
df.iloc[lambda _df: [0, 1], :]
#二维索引
df.iloc[:, 1]
df.iloc[:, 0:3]  #取前三列，注意3结尾只到编号2的行
df.iloc[:, [0,1,2]]
df.iloc[:, [True,True,True,False]] # 前三列（布尔数组长度等于行数）
df.iloc[:, df.loc['a']>0] #×
df.iloc[:, df.iloc[0]>0]  #×
df.iloc[:, lambda _df: [0, 1]]

#精准取值
df.at['a', 'A']
df.iat[0, 0]