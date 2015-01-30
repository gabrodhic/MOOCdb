import community
# import matplotlib.pyplot as plt
from collections import Counter
import networkx as nx
from sklearn.cluster import SpectralClustering
from datetime import timedelta, datetime
import random
import numpy as np
import pdb
# from topics import TopicModel, Topic

def makeHash(username):
        '''
        Returns a ripemd160 40 char hash of the given name. 

        :param username: name to be hashed
        :type username: String
        :return: hashed equivalent. Calling this function multiple times returns the same string

        :rtype: String
        '''
        #return hashlib.sha224(username).hexdigest()
        oneHash = hashlib.new('ripemd160')
        oneHash.update(username)
        return oneHash.hexdigest()

class CommunityBase:
    @property
    def start_date(self):
        if not self.start:
            return "start"
        return self.start.strftime( "%Y-%m-%d %H:%M:%S")

    @property
    def end_date(self):
        if not self.end:
            return "end"
        return self.end.strftime( "%Y-%m-%d %H:%M:%S")

    def get_topics(self):
        return self.topic_model.get_topics()

    def get_output_features(self):
        return self.features

    def get_output_values(self):
        return [getattr(self, feature) for feature in self.get_output_features()]

class CommunityGraphTime(CommunityBase):
    def __init__(self, graph_data, topic_model, date_ranges):
        self.topic_model = topic_model
        self.graph_data = graph_data
        self.community_graphs = None
        self.class_community_graph = None
        self.date_ranges = date_ranges
        self.start = date_ranges[0][0]
        self.end = date_ranges[-1][1]
        self.full_class = None
        
    def get_community_graphs(self):
        if not self.community_graphs:
            self.community_graphs = self.make_community_graphs()
        
        return self.community_graphs

    def get_full_class(self):
        if not self.full_class:
            print "making full class community graph"
            self.full_class = CommunityGraph(self.graph_data, self.topic_model, self.start, self.end, -1)

        return self.full_class

    def make_community_graphs(self):
        community_graphs = []
        interval_num = 0
        for (start, end) in self.date_ranges:
            edges = self.graph_data.get_edges(start, end)
            if len(edges) < 1:
                break

            print "making community graph for interval %d" % (interval_num+1)
            community_graphs.append(CommunityGraph(self.graph_data, self.topic_model, start, end, interval_num))
            interval_num += 1
        return community_graphs

    def get_meta_topics(self):
        g,t,m = self.graph_data.get_meta_topic_mapping()

        topics = []

        topics.append(MetaTopic(self.graph_data, g, "General"))
        topics.append(MetaTopic(self.graph_data, t, "Technical"))
        topics += [MetaTopic(self.graph_data, [i], 'Topic'+ str(i2)) for i, i2 in zip(m, range(len(m)))]

        return topics

    def get_all_communities(self):
        communities = []
        self.community_graphs =self.get_community_graphs()
        for c in self.community_graphs:
            communities += c.communities
        return communities

    def get_all_students(self):
        students = []
        for c in self.get_all_communities():
            students += c.students
        return students

        
class CommunityGraph(CommunityBase):
    features = ["num_communities", "num_students", "average_community_size", "max_community_size", "modularity",'num_threads' , 'num_threads_no_reply', "num_posts", "num_edges", "communities_per_duration", "posts_per_duration", "posts_per_community", "top_topic", 'start_date', 'end_date', "duration_days", 'interval_num']

    def __init__(self, graph_data, topic_model, start, end, interval_num, n_clusters=0):
        # super(CommunityGraph, self).__init__()
        self.start = start
        self.end = end
        self.interval_num = interval_num
        self.graph_data = graph_data
        self.topic_model = topic_model
        self.threads = self.graph_data.get_thread_text(start=start, end=end)
        self.topic_dist = self.get_topic_distribution()
        edges = graph_data.get_edges(start, end)
        self.graph = self.build_graph(edges)
        self.partition = self.louvian_partition()
        self.communities = self.make_communities(n_clusters)

    def get_topic_distribution(self):
        return self.topic_model.get_topic_distribution(self.threads)

    def build_graph(self, edges):
        """
        input: list of directed edges (node, neighbor, weight)
        output: networkx.Graph
        """
        g = nx.Graph()
        for node, neighbor, weight in edges:
            #handling conversion from directed edges to undirected graph
            if neighbor in g and node in g[neighbor]:
                g[neighbor][node]['weight'] += weight
            else:
                g.add_edge(node, neighbor, weight=weight)
        
        return g

    def make_communities(self, n_clusters=0):
        partition = self.partition
        communities = []
        
        for name in set(partition.values()):
            subgraph = self.graph.subgraph([node for node in partition if partition[node] == name])
            communities.append(Community(name, self.graph_data, self.topic_model, subgraph, self.graph, self.start, self.end, self.interval_num))

        return communities

    def get_topic_num_hist(self):
        return self.topic_model.get_topic_num_hist(self.threads)
        

    def louvian_partition(self):
        partition = community.best_partition(self.graph)
        return partition

    def community_sizes(self):
        return [c.num_students for c in self.communities]

    @property
    def average_community_size(self):
        s = self.community_sizes()
        return float(sum(s))/len(s)

    @property
    def median_community_size(self):
        s = self.community_sizes()
        return np.median(s)
    
    @property
    def max_community_size(self):
        s = self.community_sizes()
        return max(s)

    @property
    def num_communities(self):
        return len(self.communities)

    @property
    def num_students(self):
        return len(self.graph.nodes())        

    @property
    def modularity(self):
        return community.modularity(self.partition, self.graph)

    @property
    def num_edges(self):
        return self.graph.size()

    @property
    def num_posts(self):
        return self.graph.size(weight='weight')

    @property
    def duration_days(self):
        if not self.end and not self.start:
            return "full_class_duration"
        return float((self.end - self.start).days)

    @property
    def communities_per_duration(self):
        if not isinstance(self.duration_days, float):
            return "n/a"
        return self.num_communities/self.duration_days

    @property
    def posts_per_duration(self):
        if not isinstance(self.duration_days, float):
            return "n/a"
        return self.num_posts/self.duration_days

    @property
    def posts_per_community(self):
        return float(self.num_posts)/self.num_communities
    
    @property
    def num_threads(self):
        return len(self.graph_data.get_thread_text(start=self.start, end=self.end))

    @property
    def num_threads_no_reply(self):
        return self.graph_data.num_threads_no_reply(start=self.start, end=self.end)

    @property
    def top_topic(self):
        return self.topic_dist.index(max(self.topic_dist))

    def get_output_features(self):
        topic_features = ["topic"+str(i) for i in range(len(self.topic_dist))]
        return self.features+topic_features

    def get_output_values(self):
        return [getattr(self, feature) for feature in self.features]+self.topic_dist

class Community(CommunityBase):
    features = ["community_id", "num_threads", "num_students", "num_inside_edges","num_posts", "num_outside_edges", "posts_per_duration", 'start_date', 'end_date', "interval_num", "duration_days"]

    def __init__(self, community_id, graph_data, topic_model, subgraph, graph, start, end, interval_num):

        self.community_id = community_id
        self.graph_data = graph_data
        self.topic_model = topic_model
        self.subgraph = subgraph
        self.graph = graph
        self.start = start
        self.end = end
        self.interval_num = interval_num
        self.threads = self.get_threads(start, end)
        self.topic_dist = self.get_topic_distribution()
        # self.students = self.make_students()

    def make_students(self):
        # pdb.set_trace()
        student_posts = self.graph_data.get_student_posts(self.start, self.end)
        students = []
        for node in self.subgraph:
            node = str(node)
            num_replies_posted = 0
            num_threads_started = 0
            num_replies_recieved = 0
            if node in student_posts:
                num_replies_posted = student_posts[node].get("Comment", 0)
                num_threads_started = student_posts[node].get("CommentThread", 0)
            
            num_replies_recieved = self.graph.degree(node, 'weight') - num_replies_posted  #total interations minus num posts implies the num of replies

            if num_replies_posted + num_threads_started + num_replies_recieved <= 0:
                # pdb.set_trace()
                raise Exception("%s had no iteractions in this time period, so they cannot be in this community." % (node))

            if num_replies_recieved<0:
                # pdb.set_trace()
                raise Exception("negative number of replies for %s which is impossible." % (node))

            students.append(Student(node, self.graph_data, self.topic_model, num_replies_posted, num_threads_started, num_replies_recieved,  self.community_id, self.start, self.end, self.interval_num))
        return students

    def get_threads(self, start=None, end=None):
        author_usernames = [n for n in self.subgraph]
        threads = self.graph_data.get_thread_text(author_usernames = author_usernames, start=start, end=end)
        return threads

    def get_topic_distribution(self):
        return self.topic_model.get_topic_distribution(self.threads)

    @property
    def num_students(self):
        return self.subgraph.number_of_nodes()

    @property
    def num_threads(self):
        return len(self.threads)

    @property
    def num_inside_edges(self):
        return self.subgraph.number_of_edges()

    @property
    def num_posts(self):
        return self.subgraph.size(weight='weight')

    @property
    def duration_days(self):
        if not self.end and not self.start:
            return "full_class_duration"
        return float((self.end - self.start).days)

    @property
    def posts_per_duration(self):
        if not isinstance(self.duration_days, float):
            return "n/a"
        return self.num_posts/self.duration_days

    @property
    def num_outside_edges(self):
        count = 0
        for node in self.subgraph:
            count += len(self.graph.neighbors(node))

        return count - self.num_inside_edges #we  din'tdouble counted inside edges during iteration because it is directed graph



#convert things to attributes
class Student(CommunityBase):
    def __init__(self, name, graph_data, topic_model, num_replies_posted, num_threads_started, num_replies_recieved, community_id,  start, end, interval_num):
        self.node_id = name
        self.start = start
        self.end = end
        self.interval_num = interval_num
        self.graph_data = graph_data
        self.topic_model = topic_model
        self.community_id = community_id
        self.topic_model = topic_model
        self.threads = [] #number of threads this student posted in
        self.num_replies_posted = num_replies_posted
        self.num_threads_started = num_threads_started
        self.num_replies_recieved = num_replies_recieved
        self.interval_num = interval_num

        if num_replies_posted + num_threads_started > 0:
            self.threads = self.graph_data.get_thread_text(author_usernames=[self.node_id], start=self.start, end=self.end)

        self.topic_dist =  self.get_topic_dist()


    def get_topic_dist(self):
        topic_dist = self.topic_model.get_topic_distribution(self.threads)

        return topic_dist

    def get_output_features(self):
        return ["node_id", "community_id", "num_threads", "num_replies_posted", 'num_threads_started', 'num_replies_recieved'] +["topic"+str(x) for x in range(self.topic_model.num_topics)] + ['start_date', 'end_date', "interval_num"]

    def get_output_values(self):
        topic_dist = self.topic_dist
        num_threads = len(self.threads)
        # num_posts = self.graph_data.get_user_posts(author_username=self.node, start=self.start, end=self.end)
        return [makeHash(self.node_id), self.community_id, num_threads, self.num_replies_posted, self.num_threads_started, self.num_replies_recieved] + topic_dist + [self.start_date, self.end_date, self.interval_num]




# def get_first_last_date(self):
    #     """
    #     Try to detect when the class ended and return the proper date range.
    #     This is useful because sometimes the datasource has posts from after the class was over
    #     """
    #     first, last = self.graph_data.get_first_last_date()
    #     return first, last
    #     start = first
    #     delta = timedelta(days = 7)
    #     posts = []
    #     last_num_posts = None

    #     while start < last:
    #         end = min(start + delta, last)
    #         num_posts = len(self.graph_data.get_thread_text(start=start, end=end))
    #         posts.append(num_posts)
    #         posts = posts[-3:]

    #         if last_num_posts == None:
    #             last_num_posts = num_posts
    #             start = end
    #             continue

    #         avg_posts = float(sum(posts))/len(posts)

    #         # print avg_posts, num_posts
    #         #when course lasts the diff should go way up and be negative
    #         if num_posts < .5*avg_posts and num_posts<100:
    #             print "end course early"
    #             # reverse one step
    #             end = start
    #             break

    #         last_num_posts = num_posts
    #         start = end

    #     return first, end