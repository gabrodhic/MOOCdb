"""
Created 8/4/2014 by Kevin Wen

Pairs duplicate problems from different offerings of 6.002x and matches their problem_ids.
These values are printed onto the terminal screen.
"""

import MySQLdb
import time
import csv

def match_problem_id(cursor, problemList):
    #for each problem_id
    for problem_id in problemList:
	query = """SELECT problem_name
		FROM problems
		WHERE problem_id = %s;
		"""%(str(problem_id))
	cursor.execute(query)
	temp = cursor.fetchall()
	arr_temp = list(temp[0][0])
	arr_temp[12] = '_' # Corrects the formatting differences between both databases
	string = ''.join(arr_temp)
	query = """SELECT a.problem_id
		FROM 6002x_fall_2012.problems AS a
		WHERE a.problem_name = '%s'
		;
		"""%(string)
    	cursor.execute(query)
    	temp = cursor.fetchall()
	if len(temp) == 0:
	    mapping = "NaN" # problem_id has no counterpart
	else:
	    mapping = temp[0][0]
	print "F2012 | S2013 : %s | %s"%(mapping, problem_id)


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
    for x in range(54,55):
        problemList.append(x)
                        
    match_problem_id(cursor, problemList)


    db.close()
