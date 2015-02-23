"""
Created: 8/12/14 by Kevin Wen
Generates a csv file of a single student's submission history, ordered by submission timestamp.

FORMAT:
1) problem_id 2) submission_timestamp 3) submission_attempt_number 4) assessment grade (1 or 0)
"""

import MySQLdb
import time
import csv
import os
import glob
import sys


def generate_user_csv(cursor):

# Selects the problem with the most users
    query = """SELECT problem_id, COUNT(DISTINCT user_id)
FROM submissions
GROUP BY problem_id
ORDER BY COUNT(user_id) DESC;
"""
    cursor.execute(query)
    problem = cursor.fetchone()
    problem_id = problem[0]

# Selects all the users who attempted the given problem_id
    query = """SELECT DISTINCT user_id
FROM submissions
WHERE problem_id = %s;"""%str(problem_id)
    cursor.execute(query)
    students = cursor.fetchall()
    print "Total number of students: %i"%len(students)
    limit = 0
    for student in students:
	
        print "Generating csv for student %s, date: %s"%(student,time.strftime("%y%m%d"))
        filename = "%s.csv"%student
        f=open(filename,'wb')
        f.close()
        query = """SELECT s.problem_id, s.submission_timestamp, s.submission_attempt_number, a.assessment_grade
FROM submissions AS s
INNER JOIN assessments AS a
ON s.submission_id = a.submission_id
WHERE s.user_id = "%s"
ORDER BY s.submission_timestamp ASC;"""%(student)
	cursor.execute(query)
        with open(filename,'a') as csvfile:
            writer = csv.writer(csvfile)
	    previous = cursor.fetchone()
	    if previous != None:
		writer.writerow(list(previous))
		next = cursor.fetchone()
		while next !=None:
		    if next[1] != previous[1]:   
    	        	writer.writerow(list(next))
		        previous = next
		    next = cursor.fetchone()
	limit+=1
	if limit>3: # Stops after 10 users have been generated
	    sys.exit()
                    
if __name__ == "__main__":
    
    host = "alfa6.csail.mit.edu"
    port = 3306
    user = "kevin"
    dbS2013 = "moocdb_6002x_spring_2013"
    dbF2012 = "6002x_fall_2012"
    dbS2012 = "moocdb"
    pw = "cosmos5"

    db = MySQLdb.connect(host=host, port=port, user=user, db=dbF2012, passwd=pw)
    cursor = db.cursor()
                        
    generate_user_csv(cursor)


    db.close()
