import pymongo
from data import MongoMOOC
from topics import TopicModel
from sklearn.metrics.pairwise import cosine_similarity
from gensim.matutils import corpus2csc

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pylab as pl

def find(i2):
	i1 = similarity.argmax(0)[i2]
	print "Thread:\n" + t2[i2] + "\n"
	print "related thread:\n" + t1[i1]
	print  "topic diffs: ", t1_topics[i1].todense() -  t2_topics[i2].todense()
	print "max: ", similarity.max(0)[i2]
	print 'cosine_similarity: ', cosine_similarity(t1_topics[i1], t2_topics[i2])

# classes = ["mitx_3_091x_2012_fall", "mitx_3_091x_2013_spring"]
# classes = ["mitx_6_002x_2012_fall", "mitx_6_002x_2013_spring"]

# client = pymongo.MongoClient("localhost", 27017)
# offering1 = MongoMOOC(client[classes[0]])
# offering2 = MongoMOOC(client[classes[1]])

# t1 = offering1.get_thread_text()
# t2 = offering2.get_thread_text()

# topic_model = TopicModel(50, 10)
# topic_model.build(t1+t2)


# t1_topics = corpus2csc(topic_model.model_docs(t1)).T
# t2_topics = corpus2csc(topic_model.model_docs(t2)).T

# similarity = cosine_similarity(t1_topics, t2_topics)


# pl.pcolor(similarity)
# pl.colorbar()
# pl.title("6.002 Fall 2012/Spring 2013 Thread similarity")
# pl.xlabel("Second offering threads")
# pl.ylabel("First offering threads")
# pl.savefig("6002x_similarity")



classes = ["mitx_3_091x_2012_fall", "mitx_3_091x_2013_spring"]
# classes = ["mitx_6_002x_2012_fall", "mitx_6_002x_2013_spring"]

client = pymongo.MongoClient("localhost", 27017)
offering1 = MongoMOOC(client[classes[0]])
offering2 = MongoMOOC(client[classes[1]])

t1 = offering1.get_thread_text()
t2 = offering2.get_thread_text()

t1 = [x for x in t1 if len(x) > 400]
t2 = [x for x in t2 if len(x) > 400]

topic_model = TopicModel(50, 10)
topic_model.build(t1+t2)


t1_topics = corpus2csc(topic_model.model_docs(t1)).T
t2_topics = corpus2csc(topic_model.model_docs(t2)).T

similarity = cosine_similarity(t1_topics, t2_topics)

pl.pcolor(similarity)
pl.colorbar()
pl.title("3.091 Fall 2012/Spring 2013 Thread similarity")
pl.xlabel("Second offering threads")
pl.ylabel("First offering threads")
pl.savefig("3091x_similarity")

print similarity





