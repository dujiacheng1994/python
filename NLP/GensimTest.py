from gensim.models.word2vec import Word2VecKeyedVectors

file = r"C:\Users\Administrator\Downloads\Tencent_AILab_ChineseEmbedding\Tencent_AILab_ChineseEmbedding.txt"
model = Word2VecKeyedVectors.load_word2vec_format(file, binary=False)

try:
    sim1 = model.similarity(u'沙瑞金', u'高育良')
    sim2 = model.similarity(u'李达康', u'易学习')

except KeyError:
    sim1 = 0
    sim2 = 0
print(u'沙瑞金 和 高育良 的相似度为', sim1)
print(u'李达康 和 易学习 的相似度为', sim2)

#计算某个词的相关列表
try:
    sim3=model.most_similar(u'小鸟',topn=100)
    print(u'和 小鸟 与相关的词有: \n')
    for key in sim3:
        print(key[0],key[1])
except:
    print( 'error')


#与某个词最相近的3个字的词
print(u'最相近的3个字的词')
req_count=5  #求出5个与之相近的3个字的词
word = u'太阳'
for key in model.similar_by_word(word,topn=100):
    if len(key[0])==len(word):   #key[0]应该就表示某个词
        req_count-=1
        print(key[0],key[1])  #某一个词,某一个词出现的概率
        if req_count==0:
            break