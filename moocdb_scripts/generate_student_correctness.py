"""
Created 8/12/14 by Kevin Wen
Generates a csv file of a single student's correctness history (ordered chronologically) for every single problem.

File name is %i.csv where %i is a positive integer counting up starting from 1.

FORMAT:
1) problem_id 2) String of submission grades (0's and 1's e.g. 0001)
"""

import MySQLdb
import time
import csv
import os
import glob
import sys


def generate_user_csv(cursor):

# Selects problem with most users
   query = """SELECT problem_id, COUNT(DISTINCT user_id)
FROM submissions
GROUP BY problem_id
ORDER BY COUNT(user_id) DESC;
"""
   cursor.execute(query)
   problem = cursor.fetchone()
   problem_id = problem[0]
# Selects users from problem_id
    query = """SELECT DISTINCT user_id
FROM submissions
WHERE problem_id = %s;"""%str(problem_id)
    cursor.execute(query)
    students = cursor.fetchall()

    print "Total number of students: %i"%len(students)

    limit = 0
    num = 0
    for student in students:
	    num += 1
        print "Generating csv for student %s, date: %s"%(student,time.strftime("%y%m%d"))
        filename = "%i.csv"%num
        f=open(filename,'wb')
        f.close()

        query = """SELECT s.problem_id, a.assessment_grade
FROM submissions AS s
INNER JOIN assessments AS a
ON s.submission_id = a.submission_id
WHERE s.user_id = "%s"
ORDER BY s.problem_id,s.submission_timestamp ASC;"""%(student)

	cursor.execute(query)
	previous = cursor.fetchone()
	ansline = ""
	while previous != None:
	    ansline += str(int(previous[1]))
	    next = cursor.fetchone()
	    if next != None:
		if next[0] != previous[0]:
		    with open(filename,'a') as csvfile:
            		writer = csv.writer(csvfile)
			writer.writerow((previous[0],ansline))
			ansline = ""
	    previous = next
	limit+=1
	if limit>10: # Stops after 10 users have been generated
	    sys.exit()	
                    
if __name__ == "__main__":
    
    host = "localhost"
    port = 3316
    user = "root"
    database = "newtest"
    pw = "toor"

    db = MySQLdb.connect(host=host, port=port, user=user, db=database, passwd=pw)
    cursor = db.cursor()
                        
    generate_user_csv(cursor)


    db.close()
