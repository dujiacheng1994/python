import pandas as pd
import pymysql
#建立连接
try:
    #conn = pymysql.connect(host='120.79.223.179',port= 3306,user = 'root',passwd='hz123456',db='huibenxia_test')
    conn = pymysql.connect(host='localhost',port= 3306,user = 'root',passwd='root',db='huibenxia_test_du')  #todo:本地测试时检查一下是不是local,防误导入hezi的库
    cur = conn.cursor()
    #读取Excel文件
    sheet = 0
    df=[]
    while sheet < 6:
        df.append(pd.read_excel(r'C:\Users\Administrator\Desktop\345.xlsx',sheet_name=sheet))
        sheet = sheet + 1

    f = open(r'urls.txt', "a", encoding='utf-8-sig')
    base_picbookid = 7    #todo:每次记得修改

    sql = "select ifnull((select max(id) from page), 0)"  #获取当前页面起始id
    cur.execute(sql)
    base_pageid = cur.fetchall()[0][0]  # 得到tuple, a[0][0]表示第1行第1列
    sql = "select ifnull((select max(id) from image), 0)"  #获取当前图片起始id
    cur.execute(sql)
    base_imageid = cur.fetchall()[0][0]
    sql = "select ifnull((select max(id) from role), 0)"  #获取当前角色起始id
    cur.execute(sql)
    base_roleid = cur.fetchall()[0][0] + 1

    #picbook插入
    url_bmg = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/bgimage/背景.jpg'
    url_bgm = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/bgmusic/bgMusic.mp3'
    url_mapbmg = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/map/map背景.png'
    f.write(url_bgm + '\n')
    f.write(url_bmg + '\n')
    sql=("insert into picbook (id,name,home_background_image_url,background_music_url,map_background_image_url) values ('%s','%s','%s','%s','%s');") % (base_picbookid,df[0]._get_values[0][0],url_bmg,url_bgm,url_mapbmg)
    cur.execute(sql)
    #conn.commit()
    print('picbookok')
    #page插入
    for n in range(len(df[1])):
        sql= "insert into page (name,picbook_id,sort,background_image_url,voice_text,story_code) values ('%s','%s','%s','%s','%s','%s');" % (df[1]._get_values[n][0], base_picbookid, df[1]._get_values[n][1], 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/picbook-'+str(base_picbookid)+'/page'+str(df[1]._get_values[n][1])+'/背景.jpg', df[1]._get_values[n][2], df[1]._get_values[n][3])
        cur.execute(sql)
    #conn.commit()
    print('pageok')
    #role插入
    imageid = base_imageid
    for m in range(len(df[2])):   #基于角色个数循环
        #插入角色图
        imageid = imageid + 1
        url_role = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/page'+str(df[2]._get_values[m][1])+'/'+str(df[2]._get_values[m][0])+'.png'
        f.write(url_role + '\n')
        sql = ("insert into image (id,url,x,y,z,width,height) values ('%s','%s','%s','%s','%s','%s','%s');") % (imageid,url_role, str(100*df[2]._get_values[m][2])[:5]+str('%'),str(100*df[2]._get_values[m][3])[:5]+str('%'), df[2]._get_values[m][4],str(100*df[2]._get_values[m][5])[:5]+str('%'),str(100*df[2]._get_values[m][6])[:5]+str('%'))
        cur.execute(sql)
        sql = ("insert into role (name,page_id,image_id) values ('%s','%s','%s');") % (df[2]._get_values[m][0], base_pageid+df[2]._get_values[m][1],imageid)
        cur.execute(sql)
        if len(df[4]) != 0:  # 若解释图不为空，插入解释图 todo:以后该循环要拿出来，当会出现无法一一对应的情况时
            imageid = imageid + 1
            url_role_explain = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/page'+str(df[2]._get_values[m][1])+'/'+str(df[2]._get_values[m][0])+'卡.png'
            f.write(url_role_explain+'\n')
            sql = ("insert into image (id,url,x,y,z,width,height) values ('%s','%s','%s','%s','%s','%s','%s');") % (imageid,url_role_explain, str(100*df[4]._get_values[m][2])[:5]+str('%'),str(100*df[4]._get_values[m][3])[:5]+str('%'),'null',str(100*df[4]._get_values[m][4])[:5]+str('%'),str(100*df[4]._get_values[m][5])[:5]+str('%'))
            cur.execute(sql)
            sql = ("insert into explaination (role_id,image_id) values ('%s','%s');") % (base_roleid +m, imageid)
            cur.execute(sql)
    if len(df[4]) == 0:
        # 否则插入对话图
        for i in range(len(df[5])):
            imageid = imageid + 1
            url_dialogue = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/common/chat-image/' + str(df[5].get_values()[i][7]) + '.png'
            f.write(url_dialogue + '\n')
            sql = ("insert into image (id,url,x,y,z,width,height) values ('%s','%s','%s','%s','%s','%s','%s');") % (imageid, url_dialogue, str(100 * df[5]._get_values[i][2])[:5]+str('%'), str(100 * df[5]._get_values[i][3])[:5]+str('%'),'null', str(100 * df[5]._get_values[i][4])[:5]+str('%'), str(100 * df[5]._get_values[i][5])[:5]+str('%'))
            cur.execute(sql)
            # 依对白名字找role顺序
            row = 0
            while (df[5].get_values()[i][0] != df[2].get_values()[row][0]) | (df[5].get_values()[i][1] != df[2].get_values()[row][1]):
                row = row + 1
            sql = ("insert into dialogue (role_id,role_name,image_id,angle,dialog_context) values ('%s','%s','%s','%s','%s');") % (base_roleid + row, df[2]._get_values[row][0], imageid, 0, df[5]._get_values[i][6])  # todo: 此处有bug
            cur.execute(sql)
    #conn.commit()
    print('roleok')
    #imagery插入
    for p in range(len(df[3])):  #基于意象个数循环
        imageid = imageid + 1
        #插入意象图
        url_imagery = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/page'+str(df[3]._get_values[p][6])+'/'+str(df[3]._get_values[p][0])+'.png'
        f.write(url_imagery+'\n')
        sql = ("insert into image (id,url,x,y,z,width,height) values ('%s','%s','%s','%s','%s','%s','%s');") % (imageid, url_imagery, str(100*df[3]._get_values[p][1])[:5]+str('%'), str(100*df[3]._get_values[p][2])[:5]+str('%'),df[3]._get_values[p][3],str(100*df[3]._get_values[p][4])[:5]+str('%'),str(100*df[3]._get_values[p][5])[:5]+str('%'))
        cur.execute(sql)
        #插入意象icon图
        url_icon1 = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/icon/1st/'+str(df[3]._get_values[p][0])+'.png'
        url_icon2 = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/icon/2nd/'+str(df[3]._get_values[p][0])+'.png'
        url_icon3 = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/icon/3rd/'+str(df[3]._get_values[p][0])+'.png'
        f.write(url_icon1+'\n')
        f.write(url_icon2+'\n')
        f.write(url_icon3+'\n')
        sql = ("insert into thumbnail (id,url1,url2,url3) values ('%s','%s','%s','%s');") % (imageid,url_icon1,url_icon2,url_icon3)
        cur.execute(sql)
        #插入意象表项/解释图
        url_imagery_explain = 'https://hz-huibenxia.oss-cn-shenzhen.aliyuncs.com/3658-1995/picbook-'+str(base_picbookid)+'/card/'+str(df[3]._get_values[p][0])+'卡.png'
        f.write(url_imagery_explain + '\n')
        sql = ("insert into imagery (page_id,thumbnail_id,background_image_id,card_text,explain_image_url,category_code) values ('%s','%s','%s','%s','%s','%s');") % (base_pageid+df[3]._get_values[p][6],imageid,imageid,df[3]._get_values[p][0],url_imagery_explain,df[3]._get_values[p][7])
        cur.execute(sql)
    conn.commit()
    print('imageok')
# except Exception as e:
#     conn.rollback()  #todo:为防以后插入出错，入库不完全
#     print(e)
finally:
    conn.close()

#todo： 规范循环变量

