"""
Created: 3/5/2014
Last modified: 7/8/2014

Version 2
Generated new csv files that have less columns than before

FILE NAME: problem_%i_f2012.csv e.g. problem_330_f2012.csv

FORMAT
1) user_id 2) timestamp 3)resource_id 4) duration 5) 0

1) user_id 2) timestamp 3) submission status 4) correctness (1 or 0)
5) 1 for correct, 2+ for different incorrect answers

Different codes for the submission status
     1 : Answer is submitted
     0 : Answer is saved
     2 : Failure 
     3 : Reset
    -1 : Other  

FILTERS on observed events
1. remove consecutive repeated events (defined as consecutive events with same timestamp AND same resource id AND same duration)
2. remove events less than min_time
3. remove consecutive events with the same resource id

FILTERS on submission events
1. remove consecutive events of the same user submitting the same answer

"""

import MySQLdb
import time
import csv
import os
import glob


def generate_csv_file_by_problem(cursor, problemList, min_time=10, certified=False, numOfAnswerCate=10):
    """
cursor: db cursor
problemList: list of problem id to be generated
certified: all users or only the certified users
min_time: filter for cutting off events with duration under min_time in seconds
numOfAnswerCate: group answers into how many categories by correctness and count
0 = resource, 1 = correct, 2-numOfAnswerCate = top incorrect answers
"""
    #for each problem_id
    for problem_id in problemList:
        print "Generating csv for problem %i, date: %s"%(problem_id,time.strftime("%y%m%d"))
        if certified:
            filename = "problem_csv_short/problem_c_%i_v3.csv"%(problem_id)
        else:
            filename = "problem_%i_f2012.csv"%(problem_id)
        f=open(filename,'wb')
        f.close()
        
        #get list of students
        query = """SELECT DISTINCT s.user_id
FROM submissions AS s
"""
        if certified:
            query += """INNER JOIN users AS u
ON u.user_id = s.user_id
WHERE u.user_final_grade >= 0.5
AND s.problem_id = %s;
"""%str(problem_id)
        else:
            query += "WHERE s.problem_id = %s;"%str(problem_id)
        cursor.execute(query)

        students = cursor.fetchall()
        print "Total number of students: %i"%len(students)
            
        #get top incorrect answers ordered by count
        d=countIncorrectAnswer(cursor,problem_id,numOfAnswerCate-2)
        answerDict = topIncorrectCategory(d)
    
        lengthOfFile = 0
        t = time.time()
        # for each user:
        for user in students:
	    all_responses = []
            user_id = user[0]
            #all submission from this user for this problem
            query = """SELECT s.user_id, s.submission_timestamp, a.assessment_grade, s.submission_answer, s.submission_attempt_number
FROM submissions AS s
INNER JOIN assessments AS a
ON s.submission_id = a.submission_id
WHERE s.problem_id = %s
AND s.user_id = "%s"
ORDER BY s.submission_timestamp ASC
; 
"""%(str(problem_id),str(user_id))

            cursor.execute(query)
            all_responses = cursor.fetchall()

            if len(all_responses)>1:
                #timestamp when user first answered the problem
                first_time = all_responses[0][1]
              
                #timestamp when user last answered the problem
                last_time = all_responses[-1][1]
            elif len(all_responses)==1: #accounts for the user submitting the right answer the first time
            	with open(filename,'a') as csvfile:
                    writer = csv.writer(csvfile)
                    if all_responses[0][2] == 1: # is correct, answer category is always 1
                        answerID = 1
                    elif all_responses[0][3] in answerDict: #is top incorrect answer
                        answerID = answerDict[all_responses[0][3]]
                    else:
                        answerID = numOfAnswerCate
                    writer.writerow(list(all_responses[0])[:2]+[all_responses[0][4],int(all_responses[0][2]),answerID])
		continue
	    else:
		continue

            #all observed_events from this user between the time period
            query = """SELECT e.user_id, e.observed_event_timestamp, e.url_id, e.observed_event_duration
FROM observed_events AS e
INNER JOIN urls as u
ON u.url_id = e.url_id
WHERE e.user_id = "%s"
AND e.observed_event_timestamp >= '%s'
AND e.observed_event_timestamp <= '%s'
ORDER BY e.observed_event_timestamp ASC
;
"""%(str(user_id),first_time,last_time)
            
            cursor.execute(query)
            all_resources = []


            #FILTERS on observed events
            #1. remove consecutive repeated events (defined as consecutive events with same timestamp AND same resource id AND same duration)
            #2. remove events less than min_time

            #get the first valid observed events ( duration > min_time)
            previous = cursor.fetchone()
            while previous != None and previous[3] < min_time:
                previous = cursor.fetchone()
                
            if previous != None:
                all_resources.append(previous)
                
                line = cursor.fetchone()
                while line!= None:
                    if line[3] >= min_time:
                        if line[2] != previous[2] or line[0] != previous[0]:
                            all_resources.append(line)
                            previous = line
                    # directly skip to next line if duration less than min_time
                    line = cursor.fetchone()

            pIndex = 0
            rIndex = 0
            lengthOfFile += len(all_resources)
            lengthOfFile += len(all_responses)

            with open(filename,'a') as csvfile:
                writer = csv.writer(csvfile)
                # merge resources and responses events together and write to csv
                
                while pIndex < len(all_responses) and rIndex < len(all_resources):
                    if all_responses[pIndex][1] < all_resources[rIndex][1]:
                        if all_responses[pIndex][2] == 1: # is correct, answer category is always 1
                            answerID = 1
                        elif all_responses[pIndex][3] in answerDict: #is top incorrect answer
                            answerID = answerDict[all_responses[pIndex][3]]
                        else:
                            answerID = numOfAnswerCate
                        if pIndex != 0: #only writes submissions with different answers or user id	
                            if all_responses[pIndex-1][0] != all_responses[pIndex][0] or all_responses[pIndex-1][3] != all_responses[pIndex][3]:
		                writer.writerow(list(all_responses[pIndex])[:2]+[all_responses[pIndex][4],int(all_responses[pIndex][2]),answerID])
                        else:
			    writer.writerow(list(all_responses[pIndex])[:2]+[all_responses[pIndex][4],int(all_responses[pIndex][2]),answerID])
                        pIndex +=1
                    else:
                	writer.writerow(list(all_resources[rIndex])+[0])
			rIndex += 1

                #enter the events left behind after one list runs out
                while pIndex < len(all_responses):
                    if all_responses[pIndex][2] == 1: # is correct, answer category is always 1
                        answerID = 1
                    elif all_responses[pIndex][3] in answerDict: #is top incorrect answer
                        answerID = answerDict[all_responses[pIndex][3]]
                    else:
                        answerID = numOfAnswerCate
                    if pIndex != 0: #only writes submissions with different answers or user id		    
                    	if all_responses[pIndex-1][0] != all_responses[pIndex][0] or all_responses[pIndex-1][3] != all_responses[pIndex][3]:
	                    writer.writerow(list(all_responses[pIndex])[:2]+[all_responses[pIndex][4],int(all_responses[pIndex][2]),answerID])
                    else:
                    	writer.writerow(list(all_responses[pIndex])[:2]+[all_responses[pIndex][4],int(all_responses[pIndex][2]),answerID])
                    pIndex +=1
                while rIndex < len(all_resources):
                    writer.writerow(all_resources[rIndex]+[0])
		    rIndex +=1

        tend = time.time()
        print "Problem id %i, time elapsed: %.2f seconds. Length of csv file: %i"%(problem_id, tend-t,lengthOfFile)
	if lengthOfFile == 0:
	    os.remove(filename)

def countIncorrectAnswer(cursor,problem_id,top=10):
    """
top: choose top n answers including empty answer '\'
"""
    answer_dict = {} #a dictonary of {answer:count}

    print "Finding all incorrect answers for problem %i"%problem_id
    answer_dict = {}
    query = """SELECT s.submission_answer, COUNT(*) AS count
FROM submissions AS s
INNER JOIN assessments AS a
ON s.submission_id = a.submission_id
WHERE s.problem_id = %s
AND a.assessment_grade = 0
GROUP BY s.submission_answer
ORDER BY count DESC
LIMIT %s
;
"""%(str(problem_id),str(top))
    cursor.execute(query)

    answers = cursor.fetchall()
    for answer in answers:
            # if want to eliminate empty answers: != r""'\\'
            answer_dict[answer[0]] = answer[1]
    return answer_dict

def topIncorrectCategory(d):
    catDict = {} #{answer: category id}
    # if want to eliminate empty answers: != r""'\\'
    l=[(v,k) for k,v in d.iteritems() ]
    l.sort(reverse=True)

    cat_id = 2 # 1 is for correct answer, 0 is for unanswered
    for count,answer in l:
        catDict[answer] = cat_id
        cat_id += 1
    return catDict
                    
if __name__ == "__main__":
    
    host = "alfa6.csail.mit.edu"
    port = 3306
    user = "kevin"
    database = "6002x_fall_2012"
    pw = "cosmos5"

    db = MySQLdb.connect(host=host, port=port, user=user, db=database, passwd=pw)
    cursor = db.cursor()
    problemList = []
    for x in range(90,1000): #change this to vary which problems to generate
        problemList.append(x)
    min_time = 10
    certified = False
    numOfAnswerCate = 10
                        
    generate_csv_file_by_problem( cursor, problemList, min_time, certified, numOfAnswerCate)


    db.close()
