# encoding=utf-8
import jieba
# jieba.set_dictionary(".\dict.txt")
# jieba.initialize()
f = open(r"wordcount.txt",encoding='utf8')
keyword_text = f.read()
f.close()
seg_list = jieba.lcut(keyword_text, cut_all=False)

print("Default Mode:", "/ ".join(seg_list))  # 精确模式

count = {}
for word in seg_list:            #  使用 for 循环遍历每个词语并统计个数
    if len(word) < 2:          # 排除单个字的干扰，使得输出结果为词语
        continue
    else:
        count[word] = count.get(word, 0) + 1    #如果字典里键为 word 的值存在，则返回键的值并加一，如果不存在键word，则返回0再加上1

list = list(count.items())         # 将字典的所有键值对转化为列表
list.sort(key=lambda x: x[1], reverse=True)     # 对列表按照词频从大到小的顺序排序
f = open(r"result.txt",mode='a',encoding='utf8')
for item in list:
    f.write(str(item[0])+','+str(item[1])+'\n')
f.close()