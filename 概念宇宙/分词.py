# encoding=utf-8
from collections import Counter
import jieba
import re

def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    outputs = open('5.txt', 'w',encoding='utf-8')  # 加载处理后的文件路径
    outputs.write(chinese)


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',encoding='utf-8').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

inputs = open('1.txt', 'r',encoding='utf-8')  # 加载要处理的文件的路径
find_chinese(inputs.read())
inputs.close()
inputs = open('5.txt', 'r',encoding='utf-8')  # 加载要处理的文件的路径
outputs = open('2.txt', 'w',encoding='utf-8')  # 加载处理后的文件路径
for line in inputs:
    line_seg = seg_sentence(line)  # 这里的返回值是字符串
    outputs.write(line_seg)
outputs.close()
inputs.close()
# WordCount
with open('2.txt', 'r',encoding='UTF-8') as fr:  # 读入已经去除停用词的文件
    data = jieba.cut(fr.read())
data = dict(Counter(data))

with open('3.txt', 'w',encoding='UTF-8') as fw:  # 读入存储wordcount的文件路径
    for k, v in data.items():
        fw.write('%s,%d\n' % (k, v))
