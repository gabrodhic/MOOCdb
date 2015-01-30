from utils import get_class_dbs
import csv

fields = ["course", "num_students", "num_posts", 'num_edges', 'edge_weight_sum', "avg_edge_weight", 'num_threads', 'num_threads_no_reply', "percent_threads_no_reply"]
print fields
rows = []
for c in get_class_dbs():
	edges = c.get_edges()
	num_students = c.get_num_students()
	num_edges = len(edges)
	edge_sum = sum(x[2] for x in edges)
	avg_edge_weight = float(edge_sum)/num_edges
	num_threads = len(c.get_thread_text())
	num_threads_no_reply = c.num_threads_no_reply()
	percent_threads_no_reply = float(num_threads_no_reply)/num_threads * 100
	r = [c.name, num_students, c.get_num_posts(), num_edges, edge_sum, avg_edge_weight, num_threads, num_threads_no_reply, percent_threads_no_reply]
	print r
	rows.append(r)

with open("couhes.csv", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fields)
        for r in rows:
            writer.writerow(r)