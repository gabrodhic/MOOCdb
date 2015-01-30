from utils import get_class_dbs
import csv

fields = ["Course", "# Students", "# Posts", '# Threads', '% Threads no reply',]
print fields
rows = []
for c in get_class_dbs():
	edges = c.get_edges()
	num_students = c.get_num_students()
	num_threads = len(c.get_thread_text())
	num_threads_no_reply = c.num_threads_no_reply()
	if num_threads == 0:
		continue
	percent_no_reply = int(float(num_threads_no_reply)/num_threads*100)
	r = [c.name, num_students, c.get_num_posts(), num_threads, percent_no_reply]
	rows.append(r)
	print r

totals = ["Total/Avg"] + map(sum, zip(*rows)[1:]) 
totals[-1] /= len(rows)
print totals
rows.append(totals)

with open("data_summary.csv", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fields)
        for r in rows:
            writer.writerow(r)