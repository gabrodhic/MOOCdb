'''
-- Takes 6500 seconds to execute

Created on Jun 26, 2013

@author: Colin for ALFA, MIT lab: colin2328@gmail.com

Modifications:
- 20130626 - franck.dernoncourt@gmail.com
            Bypass all temporary tables and CSV files so 
            that this script can run directly on MOOCdb 
- 20130629 - franck.dernoncourt@gmail.com
            problems.problem_type_id <> 2 because lecture quizzes don't have any deadline
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#	        http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb 
import datetime, re
import pytz

utc=pytz.UTC


def main():
	start = datetime.datetime.now()

	db=mdb.connect(user="root",passwd="",db="moocdb")
	db2=mdb.connect(user="root",passwd="",db="moocdb")

	cursor = db.cursor()
	cursor2 = db2.cursor()

	sql = '''
	-- Takes 6500 seconds to execute
	SELECT DISTINCT(problems.problem_name) AS problem_name, br_logs.page AS url
	FROM moocdb.problems AS problems, logs.br_logs AS br_logs
	WHERE br_logs.event LIKE CONCAT('%',  problems.problem_name, '%')
		AND event_type = 10
	LIMIT 1000;
	'''
	#cursor.execute("SELECT problem_name, url FROM test.temp_problem_name_url;")
	cursor.execute(sql)

	final = re.compile('6.002_Spring_2012/Final_Exam/')
	mid = re.compile('6.002_Spring_2012/Midterm_Exam/')
	overview = re.compile('6.002_Spring_2012/Overview/')
	w1 = re.compile('6.002_Spring_2012/Week_1/')
	w2 = re.compile('6.002_Spring_2012/Week_2/')
	w3 = re.compile('6.002_Spring_2012/Week_3/')
	w4 = re.compile('6.002_Spring_2012/Week_4/')
	w5 = re.compile('6.002_Spring_2012/Week_5/')
	w6 = re.compile('6.002_Spring_2012/Week_6/')
	w7 = re.compile('6.002_Spring_2012/Week_7/')
	w8 = re.compile('6.002_Spring_2012/Week_8/')
	w9 = re.compile('6.002_Spring_2012/Week_9/')
	w10 = re.compile('6.002_Spring_2012/Week_10/')
	w11 = re.compile('6.002_Spring_2012/Week_11/')
	w12 = re.compile('6.002_Spring_2012/Week_12/')
	w13 = re.compile('6.002_Spring_2012/Week_13/')

	for row in cursor:
		problem_name = row[0]
		url = row[1]

		if final.search(url):
			deadline = datetime.datetime(2012, 06, 11, 12, 59, 59, 0) #June 10 12:00
		elif mid.search(url):
			deadline = datetime.datetime(2012, 05, 01, 12, 59, 59, 0) #April 30 12:00
		elif overview.search(url):
			deadline = datetime.datetime(2012, 06, 11, 12, 59, 59, 0) #June 10 (no deadline, use final deadline)
		elif w1.search(url):
			deadline = datetime.datetime(2012, 03, 19, 12, 59, 59, 0) #March 18
		elif w2.search(url):
			deadline = datetime.datetime(2012, 03, 26, 12, 59, 59, 0) #March 25
		elif w3.search(url):
			deadline = datetime.datetime(2012, 04, 2, 12, 59, 59, 0) #April 1
		elif w4.search(url):
			deadline = datetime.datetime(2012, 04, 9, 12, 59, 59, 0) #April 8
		elif w5.search(url):
			deadline = datetime.datetime(2012, 04, 16, 12, 59, 59, 0) #April 15
		elif w6.search(url):
			deadline = datetime.datetime(2012, 04, 25, 12, 59, 59, 0) #April 24
		elif w7.search(url):
			deadline = datetime.datetime(2012, 04, 30, 12, 59, 59, 0) #April 29
		elif w8.search(url):
			deadline = datetime.datetime(2012, 05, 7, 12, 59, 59, 0) #May 6
		elif w9.search(url):
			deadline = datetime.datetime(2012, 05, 13, 12, 59, 59, 0) #May 12
		elif w10.search(url):
			deadline = datetime.datetime(2012, 05, 21, 12, 59, 59, 0) #May 20
		elif w11.search(url):
			deadline = datetime.datetime(2012, 05, 28, 12, 59, 59, 0) #May 27
		elif w12.search(url):
			deadline = datetime.datetime(2012, 06, 4, 12, 59, 59, 0) #June 3
		elif w12.search(url):
			deadline = datetime.datetime(2012, 06, 11, 12, 59, 59, 0) #June 10 (no deadline, use final deadline)
		else:
			deadline = datetime.datetime(2012, 06, 11, 12, 59, 59, 0) #June 10 (no deadline, use final deadline)

		print deadline
		# problems.problem_type_id <> 2 because lecture quizzes don't have any deadline
		cursor2.execute("UPDATE moocdb.problems SET problems.problem_hard_deadline='%s' WHERE problems.problem_name='%s' AND problems.problem_type_id <> 2" % (deadline, problem_name))
			
	db2.commit()

	db.close()
	db2.close()
	diff = (datetime.datetime.now() - start).total_seconds()
	print 'finished in %s seconds' % diff

if __name__ == "__main__":
	main()