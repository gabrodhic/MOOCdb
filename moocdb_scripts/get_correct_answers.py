"""
Created 7/8/14 by Kevin Wen
This displays the dictionary of correctly submitted student answers for designated problem IDs.
THe answers are ordered from most common to least common.
"""

import MySQLdb
import time
import csv

def correct_answers(cursor, problemList):
    #for each problem_id
    for problem_id in problemList:
	query = """SELECT s.submission_answer, COUNT(*) AS count
		FROM submissions AS s
		INNER JOIN assessments AS a
		ON s.submission_id = a.submission_id
		WHERE s.problem_id = %s
		AND a.assessment_grade = 1
		GROUP BY s.submission_answer
		ORDER BY count DESC;
		"""%(str(problem_id))
    	cursor.execute(query)
    	answers = cursor.fetchall()
	answerList = []
	s = ""
	for answer in answers:
	    answerList.append(answer[0])
        print "Correct answers for problem %i"%(problem_id)
	for a in answerList:
	    s = s + "%s | "%(a)
	print s

if __name__ == "__main__":
    
    host = "alfa6.csail.mit.edu"
    port = 3306
    user = ""
    dbS2013 = "moocdb_6002x_spring_2013"
    dbF2012 = "6002x_fall_2012"
    dbS2012 = "moocdb"
    pw = ""

    db = MySQLdb.connect(host=host, port=port, user=user, db=dbS2013, passwd=pw)
    cursor = db.cursor()
    problemList = []
    for x in range(638,639): #change this to vary which problems to observe
        problemList.append(x)
                        
    correct_answers(cursor, problemList)


    db.close()
