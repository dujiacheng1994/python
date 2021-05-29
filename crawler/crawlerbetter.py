import requests
import json
import os
import time
import random

def image_processing(pic_path,result_path):
    #请求获取上传url
    request_url = "https://1yiwu07216.execute-api.us-east-1.amazonaws.com/getSignedUrl"
    request_head={
        'Accept':'application/json,text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Cache-Control':'no-cache',
        'Connection':'close',
        'Content-Length':'21',
        'Content-Type':'application/json;charset=UTF-8',
        'Host':'1yiwu07216.execute-api.us-east-1.amazonaws.com',
        'Origin':'https://www.malabi.co',
        'Pragma':'no-cache',
        'Referer':'https://www.malabi.co/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    }
    request_data = json.dumps({"contentType":"png"})
    res = requests.post(request_url,data=request_data, headers=request_head)
    request_result = res.text
    urls = json.loads(request_result)
    if res.status_code != 200:
        print(res.status_code)
        res.close()
        return 0
    print("获取url：完成")
    res.close()
    time.sleep(2+random.uniform(1,3))

    #上传图片
    upload_url = urls['oneTimeUploadUrl']
    # pic_path = "8.png"
    pic_size = os.path.getsize(pic_path)
    upload_head = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Connection':'close',
        'Content-Length':'%s' % pic_size,
        'Content-Type':'png',
        'Host':'malabi-upload.s3.amazonaws.com',
        'Origin':'https://www.malabi.co',
        'Referer':'https://www.malabi.co/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    }
    with open(pic_path,"rb") as fp:  # todo:格式是否能自动适应？
        pic = fp.read()
    # with open(r"1.txt","wb") as fp2:
    #     fp2.write(pic)
    upload_data = pic
    res = requests.put(upload_url,data=upload_data, headers=upload_head)
    upload_result = res.text
    if res.status_code != 200:
        print(res.status_code)
        res.close()
        return 0
    print("上传图片：完成")
    res.close()
    time.sleep(2+random.uniform(1,3))

    #处理图片
    process_url = 'https://api.malabi.co/Camera51Server/processImageAsync'
    resulturl = urls['resultUrl']
    process_head={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Cache-Control':'no-cache',
        'Connection':'close',
        'Content-Length':'368',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'api.malabi.co',
        'Origin':'https://www.malabi.co',
        'Pragma':'no-cache',
        'Referer':'https://www.malabi.co/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    }
    #todo:时间也要做成自适应！
    date = time.localtime(time.time())
    nowdate = strTime = time.strftime("%Y-%m-%d", time.localtime())
    #process_data = "callbackURL=https%3A%2F%2Fsqs.us-east-1.amazonaws.com%2F039264183653%2F5_10fcea89-d86f-4d01-aa7b-22f245f827c3&customerId=5&forceResultImage=true&originalImageURL=https%3A%2F%2Fmalabi-upload.s3.amazonaws.com%2F2019-06-27%2F1561425722596.png&shadow=true&token=2acb46bb-d9ce-4c5f-9e7d-c0cb909418d9&trackId=2acb46bb-d9ce-4c5f-9e7d-c0cb909418d9-1561354086935-83bf&transparent=false&userId=null"
    process_data = "callbackURL=https%3A%2F%2Fsqs.us-east-1.amazonaws.com%2F039264183653%2F5_10fcea89-d86f-4d01-aa7b-22f245f827c3&customerId=5&forceResultImage=true&originalImageURL=https%3A%2F%2Fmalabi-upload.s3.amazonaws.com%2F"+str(nowdate)+"%2F"+str(resulturl[50:63])+".png&shadow=true&token=2acb46bb-d9ce-4c5f-9e7d-c0cb909418d9&trackId=2acb46bb-d9ce-4c5f-9e7d-c0cb909418d9-1561951135704-49e2&transparent=false&userId=null"
    res = requests.post(process_url,data=process_data, headers=process_head)
    t = res.text
    retrieveurls = json.loads(t)
    if res.status_code != 200:
        print(res.status_code)
        res.close()
        return 0
    print("处理图片：完成")
    res.close()
    time.sleep(2+random.uniform(1,3))


    #获取图片
    #retrieve_url = "https://d2f1mfcynop4j.cloudfront.net/01072019/5/SID_2d112a93e2f017385c3f574c3a76724b/30bafcbdf6cf4cb68bc04e1e0fcc2c06_RES.png"
    retrieve_url = "https:"+retrieveurls['response']['resultImageUrl']
    retrieve_head={
        'Accept':'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'no-cache',
        'Connection':'close',
        'Host':'d2f1mfcynop4j.cloudfront.net',
        'Referer':'https://www.malabi.co/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    }
    print("尝试获取图片")
    res = requests.get(retrieve_url,headers=retrieve_head)
    #result_path ='result.png'
    with open(result_path, 'wb') as fp:  # todo:格式是否能自动适应？自动改名
        fp.write(res.content)
        fp.close()
    if(res.status_code==200):
        print("获取图片：完成")
        res.close()
        return 1
    else:
        print("获取图片：失败")
        print(res.status_code)
        res.close()
        return 0


def dircheck(max):
    try:
        f=open("images/%s.png" % max, "rb")
        f.close()
    except Exception as e:
        print(e)
        return 0
    try:
        dir_num = "results"
        if not os.path.exists(dir_num):
            os.mkdir(dir_num)
            print("已创建%s目录" % dir_num)
    except Exception as e:
        print(e)
        return 0
    return 1


if __name__ == '__main__':
    fail = 0 #作为是否连续两次失败的指示器
    i = 1
    max = input("输入图片的最大编号：")
    if dircheck(max)==0:
        print("输入任意值程序退出")
        input()
        exit()
    while i <= int(max):
        print("开始处理图片%s" % i)
        res_code = image_processing("images/%s.png" % i, "results/%s_res.png" % i) #进行处理
        if res_code == 1:   # 若处理成功
            fail = 0
            print("图片%s处理成功" % i)
            time.sleep(30+random.uniform(10,30))
            i = i+1      # 处理下一张
        else:
            print("图片%s处理失败" % i)
            if fail == 1:
                print("连续处理异常，输入任意值程序退出")
                input()
                exit()
            else:   # 此时第一次失败，i不增加，重新尝试处理当前图片
                fail = 1
                print("处理失败，等待30min重试")
                time.sleep(1800)


