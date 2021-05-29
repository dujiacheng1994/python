from sklearn.feature_extraction.text import TfidfVectorizer
import jieba

text = "我是一条天狗呀！我把月来吞了，我把日来吞了，我把一切的星球来吞了，我把全宇宙来吞了。我便是我了！"
sentences = text.split()
sent_words = [list(jieba.cut(sent0)) for sent0 in sentences]
document = [" ".join(sent0) for sent0 in sent_words]
print(document)

tfidf_model = TfidfVectorizer().fit(document)  #fit
print(tfidf_model.vocabulary_)
sparse_result = tfidf_model.transform(document) #transform
print(sparse_result)

# tfidf_model2 = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b").fit(document)
# print(tfidf_model2.vocabulary_)
#
# # 过滤出现在超过60%的句子中的词语
# tfidf_model3 = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", max_df=0.6).fit(document)
# print(tfidf_model3.vocabulary_)
#
# tfidf_model4 = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", max_df=0.6, stop_words=["是", "的"]).fit(document)
# print(tfidf_model4.vocabulary_)