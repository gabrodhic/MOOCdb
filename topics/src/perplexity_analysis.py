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



num_topics = range(2,200, 4)
with open("perplexity.txt", 'w') as out:
	out.write("course,"+",".join([str(x) for x in num_topics]))
	out.write("\n")

count = 0

for dir_name, db_name in classes:
	try:
		count +=1 
		print 'count' + str(count)
		# if count == 3:
		# 	break

		db = client[db_name]
		graph_data = data.MongoMOOC(db)
		perplexities = []
		threads = graph_data.get_thread_text()
		hold_out_threads  = [threads.pop(random.randrange(len(threads))) for _ in range(int(len(threads)*.2))]

		for num in num_topics:
			print "class: %s, number of topics: %d" %(db_name, num)
			topic_model = TopicModel(num, 10)
			topic_model.build(threads)
			p = topic_model.log_perplexity(hold_out_threads)
			perplexities.append(p)

		with open("perplexity.txt", 'a') as out:
			out.write(db_name+",")
			out.write(",".join([str(x) for x in perplexities]))
			out.write("\n")
			

		# plt.clf()
		plt.plot(num_topics, perplexities, label=dir_name)
		plt.xlabel('Number of topics')
		plt.ylabel('Lower bound on perplexity')
		plt.title('Perplexity vs Number of Topics')
		plt.grid()
		lgd = plt.legend(loc='upper right', bbox_to_anchor=(1.35,1), prop={'size':10})
		plt.savefig("perplexity-all.png", bbox_extra_artists=(lgd,), bbox_inches='tight')
	except:
		continue


