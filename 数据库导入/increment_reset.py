import pandas as pd
import pymysql
#建立连接
try:
    #conn = pymysql.connect(host='120.79.223.179',port= 3306,user = 'root',passwd='hz123456',db='huibenxia_test')
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root',db='huibenxia_test_du')
    cur = conn.cursor()

    sql = "select ifnull((select max(id) from dialogue), 1)"
    cur.execute(sql)
    base = cur.fetchall()[0][0]
    sql = "alter table dialogue AUTO_INCREMENT = %d" % base   #字符串任意处插入%d,其后跟 % （value） 即可
    cur.execute(sql)

    sql = "select ifnull((select max(id) from explaination), 1)"
    cur.execute(sql)
    base = cur.fetchall()[0][0]
    sql = "alter table explaination AUTO_INCREMENT = %d" % base
    cur.execute(sql)

    sql = "select ifnull((select max(id) from imagery), 1)"
    cur.execute(sql)
    base = cur.fetchall()[0][0]
    sql = "alter table imagery AUTO_INCREMENT = %d" % base
    cur.execute(sql)

    sql = "select ifnull((select max(id) from page), 1)"
    cur.execute(sql)
    base = cur.fetchall()[0][0]
    sql = "alter table page AUTO_INCREMENT = %d" % base
    cur.execute(sql)

    sql = "select ifnull((select max(id) from role), 1)"
    cur.execute(sql)
    base = cur.fetchall()[0][0]
    sql = "alter table role AUTO_INCREMENT = %d" % base
    cur.execute(sql)

    #conn.commit() #仅DML语句，即数据增删改查需要commit
finally:
    conn.close()
