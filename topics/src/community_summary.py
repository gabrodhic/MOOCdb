from utils import get_class_dbs
import csv
import graph
import data
from topics import TopicModel
import utils
import numpy as np
from scipy import stats
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as onplt
import matplotlib.dates as mdates

def make_graph(x,y, x_label, y_label):
	title = x_label + " vs " + y_label
	plt.clf()
	x = np.array(x)
	y = np.array(y)

	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.xlim([0, max(x)*1.1])
	plt.ylim([0, max(y)*1.1])
	plt.title(title)

	# calc the trendline (it is simply a linear fitting)
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	line = slope*x+intercept
	plt.plot(x,line,'r-',x,y,'o')

	text = 'r^2 = {0:.2f}\n'.format(r_value**2) + 'slope = {0:.2f}'.format(slope)
	plt.annotate(text, (0.05, 0.9), xycoords='axes fraction')


	plt.savefig("community_graphs/"+title.replace(" ", "_")+'.png')

def make_histogram(x, bins=20):
	plt.clf()
	plt.hist(x, bins=bins)
	plt.xlabel("Community size")
	plt.ylabel("# of Communities")
	plt.title("Distribution of community_sizes")
	plt.savefig("community_graphs/community_sizes.png")


community_sizes = []

fields = ['Course', '# Student', "# Communities", "Mean community size", 'Median community size' "Max community size", "Modularity", "Percent threads w/ reply", "Average Posts per Student"]
print fields
rows = []

plt.clf()
plt.xlabel("Community size")
plt.ylabel("# of Communities")
plt.title("Distribution of community_sizes")

for graph_data in get_class_dbs():
	if graph_data.get_num_students() == 0:
		continue

	# if len(rows) >= 2:
	# 	break

	#build class topic model, even though we dont need it 
	topic_model = utils.make_topic_model(graph_data, 1,1) 
	#figure out date ranges to consider
	date_ranges = utils.get_date_ranges(graph_data, 21)
	#build timeline
	time = graph.CommunityGraphTime(graph_data, topic_model, date_ranges)

	c = time.get_full_class()

	s = c.community_sizes()
	community_sizes += s


	y,binEdges=np.histogram(s,bins=100, density=True)
	bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
	plt.plot(bincenters,y, marker="o")




	num_students = c.num_students
	num_threads = c.num_threads
	num_threads_no_reply = c.num_threads_no_reply
	per_reply = 1-float(num_threads_no_reply) / num_threads

	avg_num_post = float(c.num_posts)/num_students

	r = [graph_data.name, c.num_students, c.num_communities, round(c.average_community_size,1), round(c.median_community_size,1) , c.max_community_size, round(c.modularity,3), round(per_reply,1), round(avg_num_post,1)]
	rows.append(r)
	print r

plt.savefig("community_graphs/community_sizes.png")


d = np.array(rows)
num_students = d[:,1].astype(int)
num_communities = d[:,2].astype(int)
mean_community_size = d[:,3].astype(float)
median_community_size = d[:,4].astype(float)
max_community_size = d[:,5].astype(int)
modularity = d[:,6].astype(float)
per_reply = d[:,7].astype(float)
avg_num_post = d[:,8].astype(float)

make_graph(num_students, num_communities, '# Students', '# Communities')
make_graph(num_students, mean_community_size, '# Students', 'Mean community size')
make_graph(num_students, max_community_size, '# Students', 'Max community size')
make_graph(num_students, modularity, '# Students', 'Modularity')
make_graph(num_students, per_reply, '# Students', 'Percent threads with at least 1 reply')
make_graph(num_students, avg_num_post, '# Students', 'Posts per student')
make_graph(num_students, median_community_size, '# Students', 'Median community size')

import pdb
pdb.set_trace()
make_histogram(community_sizes)






with open("community_summary.csv", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fields)
        for r in rows:
            writer.writerow(r)