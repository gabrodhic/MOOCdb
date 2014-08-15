"""
Created: 8/15/2014 by Kevin Wen

Curates the assessments and submissions table from MOOCdb.

1. remove consecutive submission events of the same user submitting the same answer for the same problem
2. remove submission events with the same timestamp as a previous submission event from the same user
3. remove submission events where the submission_attempt_number field is -1
4. remove submission events where the submissions_is_submitted field is -1, 2 or 3 (reset, failure, or other)
5. remove corresponding assessment events



"""

import MySQLdb
import time
import csv
import os
import glob


def curate_moocdb(cursor, min_time=10):
    """
cursor: db cursor
min_time: filter for cutting off events with duration under min_time in seconds
"""
    problemList = []
    for x in range(1,1000): #change this to vary which problems to generate
        problemList.append(x)
    for problem in problemList: # Finds all submissions where the attempt number equals -1
	    print "Curating problem %i"%(problem)

	    query = """SELECT submission_id
	FROM submissions
	WHERE problem_id = %s
	AND submission_attempt_number = -1
	;
	"""%(str(problem))

	    cursor.execute(query)
	    data = cursor.fetchall()
	    for line in data: # Removes all submissions where attempt number equals -1
			query = """DELETE from submissions WHERE submission_id = '%s';"""%(line[0])
			cursor.execute(query)

	    query = """SELECT s.user_id, s.problem_id, s.submission_timestamp, s.submission_answer, s.submission_attempt_number, s.submission_id, s.submission_is_submitted
	FROM submissions AS s
	INNER JOIN assessments AS a
	ON s.submission_id = a.submission_id
	WHERE s.problem_id = %s
	ORDER BY s.user_id, s.submission_timestamp ASC
	; 
	"""%(str(problem))
	    cursor.execute(query)
	    data = cursor.fetchall()
	    index = 0
	    while index < len(data):
		if index != 0:
		    if (data[index][0]==data[index-1][0] and data[index][1]==data[index-1][1] and (data[index][2]==data[index-1][2] or data[index][3]==data[index-1][3])) or data[index][4]==-1 or data[index][6]==-1 or data[index][6] == 2 or data[index][6] == 3:
		        query = """DELETE from submissions
		        WHERE submission_id = '%s'
		        ;
		        """%(data[index][5])
		        cursor.execute(query)
		        query = """DELETE from assessments
		        WHERE submission_id = '%s'
		        ;
		        """%(data[index][5])
		        cursor.execute(query)
		index+=1

		    #all observed_events from this user between the time period
#	    query = """SELECT e.user_id, e.observed_event_timestamp, e.url_id, e.observed_event_duration, e.observed_event_id
#	FROM observed_events AS e
#	INNER JOIN urls as u
#	ON u.url_id = e.url_id
#	ORDER BY e.user_id, e.observed_event_timestamp ASC
#	;
#	"""%(str(user_id),first_time,last_time)
	    
#	    cursor.execute(query)


	    #FILTERS on observed events
	    #1. remove consecutive repeated events (defined as consecutive events with same timestamp AND same resource id AND same duration)
	    #2. remove events less than min_time

	    #get the first valid observed events ( duration > min_time)
	    # previous = cursor.fetchone()
	    # while previous != None and previous[3] < min_time:
	    #     previous = cursor.fetchone()
		
	    # if previous != None:
	    #     all_resources.append(previous)
		
	    #     line = cursor.fetchone()
	    #     while line!= None:
	    #         if line[3] >= min_time:
	    #             if line[2] != previous[2] or line[1] != previous or line[-1] != previous[-1]:
	    #                 all_resources.append(line)
	    #         previous = line
	    #         # directly skip to next line if duration less than min_time
	    #         line = cursor.fetchone()

#	    previous = cursor.fetchone()
#	    if previous != None:
#		line = cursor.fetchone()
#		while line!=None:
#		    if line[0]==previous[0] and line[1]==previous[1] and (line[3]==previous[3] and line[2]==previous[2]):
#		        query = """DELETE from observed_events
#		        WHERE observed_event_id = '%s'
#		        ;
#		        """%(line[4])
#		        cursor.execute(query)
#		    previous = line    
#		    line = cursor.fetchone()    

                    
if __name__ == "__main__":
    
    host = "alfa6.csail.mit.edu"
    port = 3306
    user = "kevin"
    dbS2013 = "moocdb_6002x_spring_2013"
    dbF2012 = "6002x_fall_2012"
    dbS2012 = "moocdb"
    pw = "cosmos5"

    host = "localhost"
    port = 3316
    user = "root"
    dbS2013 = "newtest"
    pw = "toor"
    db = MySQLdb.connect(host=host, port=port, user=user, db=dbS2013, passwd=pw)
    cursor = db.cursor()
    min_time = 10
                        
    curate_moocdb( cursor, min_time)


    db.close()
