import pymongo 
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import data
import logging
import random
from utils import get_classes
from topics import TopicModel

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

classes = get_classes()
print classes
client = pymongo.MongoClient("localhost", 27017)




for dir_name, db_name in classes:
	db = client[db_name]
	graph_data = data.MongoMOOC(db)
	perplexities = []
	num_topics = range(2,100, 5) + range(100, 200, 10)
	threads = graph_data.get_thread_text()
	hold_out_threads  = [threads.pop(random.randrange(len(threads))) for _ in range(int(len(threads)*.15))]

	for num in num_topics:
		print "number of topics " + str(num)
		topic_model = TopicModel(num, 10)
		topic_model.build(threads)
		p = topic_model.log_perplexity(hold_out_threads)
		perplexities.append(p)

	with open("perplexity-%s.txt"%(db_name), 'w') as out:
		out.write(",".join([str(x) for x in num_topics]))
		out.write("\n")
		out.write(",".join([str(x) for x in perplexities]))
		

	plt.clf()
	plt.plot(num_topics, perplexities)
	plt.xlabel('Number of topics')
	plt.ylabel('Lower bound on perplexity')
	plt.title('%s : Perplexity vs Number of Topics' % (db_name))
	plt.grid()
	plt.savefig("perplexity-%s.png"%(db_name))

