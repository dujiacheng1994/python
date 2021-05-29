import gensim
from gensim.similarities.index import AnnoyIndexer

fname = 'synonyms_txt_index'
#生成AnnoyIndex
# file = r"C:\Users\Administrator\Downloads\Tencent_AILab_ChineseEmbedding\Tencent_AILab_ChineseEmbedding.txt"
# model = gensim.models.KeyedVectors.load_word2vec_format(file,binary=False,unicode_errors='ignore')
# annoy_index = AnnoyIndexer(model, 100)
# annoy_index.save(fname)

#读取AnnoyIndex
# annoy_index2 = AnnoyIndexer()
# annoy_index2.load(fname)
# annoy_index2.model = model
#
# word = '人民'
# vector1 = model[word]
# approximate_neighbors = model.most_similar([vector1], topn=30, indexer=annoy_index2)