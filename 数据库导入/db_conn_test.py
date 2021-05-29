import json
import pymysql

conn = pymysql.connect(
        host = 'localhost',#mysql服务器地址
        port = 3306,#端口号
        user = 'root',#用户名
        passwd = 'root',#密码
        db = 'test',#数据库名称
        charset = 'utf8',#连接编码，根据需要填写
    )
cur = conn.cursor()#创建并返回游标
cur.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.
data = cur.fetchone()
print("Database version : %s " % data) #输出相应数据库版本
conn.close() #关闭连接