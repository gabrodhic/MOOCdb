import logging, gensim, bz2
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import logging 
import pickle
import graph
import data
import os
import pdb

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class TopicModelBase():
    def save(self, file_name):
        with open(file_name, "w") as out:
            pickle.dump(self, out)
    
    @staticmethod
    def load(file_name):
        with open(file_name, "r") as model_in:
            return pickle.load(model_in)

# class MetaTopicModel(TopicModelBase):
#     def __init__(self, num_topics=10, passes=10):
#         self.num_topics = num_topics
#         self.passes = passes
#         self.gtm = None

#     def build(self, client, text_corpus):
#         self.topic_model = TopicModel(self.num_topics, self.passes)
#         self.topic_model.build(text_corpus)

#         classes = get_classes()
#         sum_topics = np.array([0.0]*self.num_topics)

#         for dir_name, db_name in classes:
#             db = client[db_name]
#             graph_data = data.MongoMOOC(db)
#             m = graph.CommunityGraphTime(graph_data, self.topic_model).get_full_class()
#             t = np.array(m.get_topic_distribution())
#             sum_topics += t

#         sum_topics /= float(len(classes))

#         print sum_topics, "sum_topics"
#         mean = sum_topics.mean()
#         std = sum_topics.std()
#         HIGH = mean + std
#         LOW = mean - std
#         # HIGH = mean
#         # LOW = mean
#         print "mean: %f, std %f, high %f, low %f" % (mean, std, HIGH, LOW)

#         general_topics = []
#         mixed = []
#         technical_topics = []

#         for topic_i, amount in enumerate(sum_topics):
#             if amount > HIGH:
#                 general_topics.append(topic_i)
#             elif amount < LOW:
#                 technical_topics.append(topic_i)
#             else:
#                 mixed.append(topic_i)

#         self.gtm = (general_topics, technical_topics, mixed)
#         print "done calculating meta topics"
#         self.gtm = general_topics, technical_topics, mixed

#     def get_topics(self):
#         return self.topic_model.get_topics()

    # def get_meta_topic_mapping(self):
    #     pass
    #     if self.gtm:
    #         return self.gtm

    #     print "calculating topic dist for meta topics"
    #     classes = get_classes()
    #     sum_topics = np.array([0.0]*self.num_topics)

    #     for dir_name, db_name in classes:
    #         if db_name == self.db.name:
    #             continue

    #         db = self.db.connection[db_name]
    #         m = MongoMOOC(db, self.num_topics, self.passes, self.model, self.vectorizer)   
    #         t = np.array(m.get_topic_distribution())
    #         sum_topics += t


    #     sum_topics /= float(len(classes))

    #     print sum_topics, "sum_topics"
    #     mean = sum_topics.mean()
    #     std = sum_topics.std()
    #     HIGH = mean + std
    #     LOW = mean - std
    #     HIGH = mean
    #     LOW = mean
    #     print "mean: %f, std %f, high %f, low %f" % (mean, std, HIGH, LOW)
    #     general_topics = []
    #     mixed = []
    #     technical_topics = []

    #     for topic_i, amount in enumerate(sum_topics):
    #         if amount > HIGH:
    #             general_topics.append(topic_i)
    #         elif amount < LOW:
    #             technical_topics.append(topic_i)
    #         else:
    #             mixed.append(topic_i)

    #     self.gtm = (general_topics, technical_topics, mixed)
    #     print "done calculating meta topics"
    #     return general_topics, technical_topics, mixed






class TopicModel(TopicModelBase):
    def __init__(self, num_topics=10, passes=10):
        self.num_topics = num_topics
        self.passes = passes
        self.gtm = None

    def build(self, text_corpus):
        self.vectorizer = self.make_vectorizer(text_corpus)
        self.model = self.train_topic_model(text_corpus)

    def make_vectorizer(self, t):
        v = CountVectorizer(stop_words='english', min_df=.01, max_df=.5)
        v.fit(t)

        return v

    def log_perplexity(self,t):
        corpus, id2word = self.make_corpus(t)
        return self.model.log_perplexity(corpus)

    def train_topic_model(self, text_corpus, num_topics=None, passes=None):        
        if not num_topics:
            num_topics = self.num_topics

        if not passes:
            passes = self.passes

        if not self.vectorizer:
            raise Exception("must have vectorizer in order to train model")

        corpus, id2word = self.make_corpus(text_corpus)
        model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics, update_every=1, chunksize=1000, passes=passes)
        return model

    def make_corpus(self, t, v=None):
        """
        From a set of text documents, make a corpus to be used by gensim for topic modeling
        """
        v = self.vectorizer

        try:
            corpus = v.transform(t)
        except ValueError, e:
            return None, None
        
        vocab = {y:x for x,y in v.vocabulary_.iteritems()}
        corpus = gensim.matutils.Sparse2Corpus(corpus, documents_columns=False)
        return corpus, vocab

    def model_docs(self, text):
        if not self.model:
            raise Exception("must train model first")


        doc, vocab = self.make_corpus(text)
        
        if doc == None or doc == []:
            return None

        return self.model[doc] #only need first document

    def get_topic_distribution(self, threads):
        topic_dist = [0]*self.num_topics

        if len(threads) == 0:
            return topic_dist

        
        # print "start model"
        thread_topics  = self.model_docs(threads)

        



        # print "end modeling"
        for topics in thread_topics:
            if topics != None:
                for t_i, w_i in topics:
                    topic_dist[t_i] += w_i
        s = sum(topic_dist)
        
        if s ==0:
            return [0]*self.num_topics


        #remove small topics
        # for i, v in enumerate(topic_dist):
        #     v = v/s
        #     if v < 1.0/self.num_topics:
        #         topic_dist[i] = 0
        #     else:
        #         topic_dist[i] = v

        #renormalize
        s = sum(topic_dist)
        topic_dist = [i/s for i in topic_dist]

        return topic_dist

    def get_topic_num_hist(self, threads):
        topic_num_hist = [0]*(self.num_topics+1)

        if len(threads) == 0:
            return topic_dist

        # print "start model"
        thread_topics  = self.model_docs(threads)

        # print "end modeling"
        for topics in thread_topics:
            count = 0
            if topics != None:
                num_topics = len([w_i for (t_i,w_i) in topics if w_i > 0])
                topic_num_hist[num_topics] += 1

        return topic_num_hist

    def words_for_topic(self, topic_num, num_words):
        return [ (x[1].encode('utf-8'), x[0]) for x in self.model.show_topic(topic_num, num_words) ]


    def get_topics(self):
        return [Topic(self, i) for i in range(self.num_topics)]


class Topic():
    NUM_WORDS = 20
    def __init__(self, topic_model, n):
        self.topic_model = topic_model
        self.topic_number = n
        self.name = "Topic %d" % n

    def get_output_features(self):
        word_features = []
        for i in range(self.NUM_WORDS):
            word_features += ["word"+str(i), 'weight'+str(i)]
        return ["topic_number"]+word_features

    def get_output_values(self):
        output_values = [str(self.topic_number)]

        words = self.topic_model.words_for_topic(self.topic_number,self.NUM_WORDS)
        for word, weight in words:
            output_values += [word, weight]

        return output_values



class MetaTopic():
    NUM_WORDS = 40
    def __init__(self, model, topics, name):
        self.model = model
        self.topics = [Topic(self.model, i) for i in topics]
        self.name = name

    def get_output_features(self):
        word_features = ["word"+str(i) for i in range(self.NUM_WORDS)]
        return ["topic_name", "num topics"]+word_features

    def get_output_values(self):
        if len(self.topics) <= 0:
            return [self.name] + [""]*self.NUM_WORDS

        num_each = int(self.NUM_WORDS/len(self.topics))

        flat_words = []
        all_words = [self.model.words_for_topic(t.topic_number,num_each) for t in self.topics]
        for n in range(num_each):
            for word_list in all_words:
                flat_words += all_words[n::num_words]
        # all_words = [self.model.words_for_topic(t.topic_number,num_each) for t in self.topics]
        # flat_words = sum(all_words, [])
        return [self.name, len(self.topics)] + flat_words[:self.NUM_WORDS]