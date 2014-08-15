"""
Created: 8/4/2014 by Kevin Wen
Prints the number of lines in an uncurated submissions table vs. a curated submissions table

"""

import MySQLdb
import time
import csv
import os
import glob


def print_file_length(cursor, problemList):
    """
cursor: db cursor
problemList: list of problem id to be counted
"""
    totalOLength = 0
    totalNLength = 0
    #for each problem_id
    for problem_id in problemList:
        oFileLength = 0
	nFileLength = 0
        #get list of students
        query = """SELECT DISTINCT s.user_id
FROM submissions AS s
WHERE s.problem_id = %s;
"""%str(problem_id)
        cursor.execute(query)
        students = cursor.fetchall()
        if len(students) > 0:
		for user in students:
		    t = time.time()
		    all_responses = []
		    user_id = user[0]
		    #all submission from this user for this problem
		    query = """SELECT s.user_id, s.submission_timestamp, s.submission_is_submitted, a.assessment_grade, s.submission_attempt_number, s.submission_answer
	FROM submissions AS s
	INNER JOIN assessments AS a
	ON s.submission_id = a.submission_id
	WHERE s.problem_id = %s
	AND s.user_id = "%s"
	ORDER BY s.submission_timestamp ASC; 
	"""%(str(problem_id),str(user_id))

		    cursor.execute(query)
		    all_responses = cursor.fetchall()
		    oFileLength += len(all_responses)
		    cursor.execute(query)
		    previous = cursor.fetchone()
		    if previous != None:
		        nFileLength += 1
			line = cursor.fetchone()
			while line!=None:
			    if not((line[0]==previous[0] and line[5]==previous[5]) or line[2] == -1 or line[2] == 2 or line[2] == 3):
				nFileLength+=1
			    previous = line    
			    line = cursor.fetchone()    

		tend = time.time()
		print "Problem id %i, time elapsed: %.2f seconds. Length of file: %i vs. %i"%(problem_id, tend-t, oFileLength,nFileLength)
		totalOLength+=oFileLength
		totalNLength+=nFileLength
    print "%i vs. %i"%(totalOLength,totalNLength) # Original file length vs. new file length
    print float((totalOLength-totalNLength)/totalOLength) # New file length relative to the percentage of the old one
                    
if __name__ == "__main__":
    
    host = "alfa6.csail.mit.edu"
    port = 3306
    user = ""
    dbS2013 = "moocdb_6002x_spring_2013"
    dbF2012 = "6002x_fall_2012"
    dbS2012 = "moocdb"
    pw = ""

    db = MySQLdb.connect(host=host, port=port, user=user, db=dbF2012, passwd=pw)
    cursor = db.cursor()
    problemList = []
    for x in range(25,300): #change this to vary which problems to generate
        problemList.append(x)
    print_file_length( cursor, problemList)


    db.close()
