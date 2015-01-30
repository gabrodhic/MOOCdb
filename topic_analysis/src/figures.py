import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as onplt
import matplotlib.dates as mdates
import numpy as np
import math
import pdb
import networkx as nx
from sklearn.cluster import KMeans

def topic_timeline(time, title, filename):
    fig = plt.figure()
    
    ax = plt.subplot(111)

    community_graphs = time.get_community_graphs(date_ranges)[1:]

    topics = np.array([c.topic_dist for c in community_graphs]).T
    dates = [c.start for c in community_graphs]
    count = 0
    for topic in topics:
        l = "Topic"+str(count) #get it to match with MetaTopic output
        linewidth=1
        ax.plot(dates, topic, '-o', label=l,linewidth=linewidth)  
        # ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        count += 1

    ax.set_title(title, fontsize=20)
    plt.subplots_adjust(top=0.85)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('%', fontsize=16)
    scale = 1.5
    fig.set_size_inches(11*scale,8.5*scale)
    lgd = ax.legend(loc='upper right', bbox_to_anchor=(1.2,1))
    fig.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight',dpi=200)


def get_topic_num_hist(community_graph, filename):
    num_topics = community_graph.topic_model.num_topics
    hist = community_graph.get_topic_num_hist()
    ind = np.arange(num_topics+1)  # the x locations for the groups

    fig = plt.figure()
    ax = plt.subplot(111)

    ax.bar(ind, hist, width=1, color='b')

    ax.set_title("Number of topics per thread")
    ax.set_xlabel('Number of Topics')
    ax.set_ylabel('Number of Threads')
    ax.set_xlim([0,num_topics])

    fig.savefig(filename + '.png')


def community_topics(community_graph, filename):
    cluster_topics = []
    real_topics = []
    for i, c in enumerate(community_graph.communities):
        num_threads = c.num_threads
        if num_threads <= 1:
            continue

        topics = c.get_topic_distribution()
        print num_threads
        real_topics.append(topics)
        cluster_topics.append(sorted(topics))


    kmeans = KMeans(n_clusters=3)
    clusters = kmeans.fit_predict(cluster_topics)

    clusters =  sorted(zip(real_topics, clusters), key=lambda x:x[1])

    cluster_colors = {
        0 : 'r',
        1 : 'g',
        2 : 'b',
        3 : 'y'
    }

    num_communities = len(clusters)
    cols = num_communities**.5
    rows = math.ceil(num_communities/cols)+1
    num_topics = community_graph.topic_model.num_topics

    ind = np.arange(num_topics)  # the x locations for the groups


    fig = plt.figure()
    for i, c in enumerate(clusters):
        topics = c[0]
        color = cluster_colors[c[1]]

        ax = plt.subplot(rows, cols, i+1)
        ax.bar(ind, topics, width=1, color=color)
        ax.set_title("Community " + str(i), fontsize=8)
        ax.set_xlabel('Topic', fontsize=8)
        ax.set_ylabel('%', fontsize=8)
        ax.set_xlim([0,num_topics])
        ax.set_ylim([0,1.0])

        # lgd = ax.legend(loc='upper right', bbox_to_anchor=(1.2,1))
    scale = 12
    fig.set_size_inches(scale,scale*rows/cols)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    fig.savefig(filename + '.png')

def interval_community_topics(time, filename):
    interval = 0
    for community_graph in time.get_community_graphs():
        community_topics(community_graph, filename + str(interval))
        interval += 1


def interval_draw_community(time, filename):
    interval = 0
    for community_graph in time.get_community_graphs():
        draw_communities(community_graph, filename + str(interval))
        interval += 1

def draw_communities(community_graph, filename):
    def get_color(value):
        value *= 1000
        return "#" + format(int(value*99999999999999), 'x')[:6]

    size = float(len(set(community_graph.partition.values())))
    g_layout = community_graph.graph.copy()
    # print  community_graph.partition
    # g_layout.remove_edges_from([
    #     e for e in g_layout.edges_iter()
    #         if (community_graph.partition[e[0]] != community_graph.partition[e[1]] and random.random()<.997)
    # ])
    pos = nx.graphviz_layout(g_layout, prog='sfdp')
    # pos = nx.spring_layout(g_layout)
    # print [(community_graph.partition[n1], community_graph.partition[n2]) for n1,n2 in g_layout.edges_iter()]
    count = 0.
    for com in set(community_graph.partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in community_graph.partition.keys() if community_graph.partition[nodes] == com]
        
        # print get_color(count/ size)
        nx.draw_networkx_nodes(community_graph.graph, pos, list_nodes, node_size = 100,
                                    node_color =  get_color(count/ size))


    nx.draw_networkx_edges(community_graph.graph,pos, alpha=0.2)
    fig.savefig(filename + '.png')