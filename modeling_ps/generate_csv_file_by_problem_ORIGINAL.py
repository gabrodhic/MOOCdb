"""
    Edx machine version
    Created: 9/19/2013
    Last modified: 9/19/2013

    FORMAT
    1) user_id 2) timestamp 3) resource_id 4) resource_type_id
    5) duration 6) 0 7) 0 8) 2

    1) user_id 2) timestamp 3) problem_resource_id 4)resource_type_id
    5) attempt number 6) parent_id 7) child_number 8)correctness 0/1
    
"""

import MySQLdb
import time
import csv


def generate_csv_file_by_problem(cursor,problemList, min_time= 10, certified = False):
    """
    cursor: db cursor
    problemList: list of problem id to be generated
    certified: all users or only the certified users
    min_time: filter for cutting off events with duration under min_time
    
    """

    #get list of students
    query = """SELECT users.user_id
                FROM users """
    if certified:
        query += "WHERE user_final_grade >= 0.5"
    query += ";"
        
    cursor.execute(query)

    students = cursor.fetchall()
    print "Total number of students: %i"%len(students)
    

    #for each problem_id
    for problem_id in problemList:
        #print "Generating csv for problem %i"%problem_id
        filename = "problem_csv/Problem_%i.csv"%problem_id
        f=open(filename,'wb')
        f.close()
        lengthOfFile = 0
        t = time.time()
        # for each user:
        for user in students:
            user_id = user[0]

            #all submission from this user for this problem
            query = """SELECT users.user_id, s.submission_timestamp, p.problem_resource_id, res.resource_type_id, s.submission_attempt_number,
                        p.problem_parent_id, p.problem_child_number, a.assessment_grade
                    FROM users
                    INNER JOIN submissions AS s
                    ON s.user_id = users.user_id
                    INNER JOIN problems AS p
                    ON p.problem_id = s.problem_id
                    INNER JOIN assessments AS a
                    ON s.submission_id = a.submission_id
                    INNER JOIN resources as res
                    ON res.resource_id = p.problem_resource_id
                    WHERE users.user_id = %s
                    AND p.problem_id = %s
                    ORDER BY s.submission_timestamp ASC
                    ;
                
                """%(str(user_id),str(problem_id))
            
            cursor.execute(query)
            all_responses = cursor.fetchall()
            
            if len(all_responses)>0:
                #timestamp when user first answered the problem
                first_time = all_responses[0][1]

                
                #timestamp when user last answered the problem
                last_time = all_responses[-1][1]
            else:
                continue

            #all observed_events from this user between the time period
            query = """SELECT users.user_id, e.observed_event_timestamp, e.resource_id, res.resource_type_id, e.observed_event_duration
                    FROM users
                    INNER JOIN observed_events AS e
                    ON e.user_id = users.user_id
                    INNER JOIN resources as res
                    ON res.resource_id = e.resource_id
                    WHERE users.user_id = %s
                    AND e.observed_event_timestamp >= '%s'
                    AND e.observed_event_timestamp <= '%s'
                    ORDER BY e.observed_event_timestamp
                    ;
                
                """%(str(user_id),first_time,last_time)
            
            cursor.execute(query)
            all_resources = []


            #FILTERS
            #1. remove consecutive repeated events
            #2. remove events less than min time
            
            previous = cursor.fetchone()
            while previous != None and previous[4] < min_time:
                previous = cursor.fetchone()
            if previous != None:
                all_resources.append(previous)
                
                line = cursor.fetchone()
                while line!= None:
                    if line[4] >= min_time:
                        if line[2] != previous[2] or line[1] != previous[1] or line[-1] != previous[-1]:
                            all_resources.append(line)
                            previous = line
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
                        writer.writerow(all_responses[pIndex])
                        pIndex +=1
                    else:
                        writer.writerow(list(all_resources[rIndex])+[0,0,2]) # for resources, the parent_id and child_number are assigned 0 and grade is all assigned 0
                        rIndex +=1

                #enter the events left behind after one list runs out
                while pIndex <  len(all_responses):
                    writer.writerow(all_responses[pIndex])
                    pIndex +=1
                while rIndex < len(all_resources):
                    writer.writerow(all_resources[rIndex]+[0,0,2]) # for resources, the parent_id and child_number are assigned 0 and grade is all assigned 0
                    rIndex +=1
        tend = time.time()
        print "Problem id %i, time elapsed: %.2f seconds. Length of csv file: %i"%(problem_id, tend-t,lengthOfFile)
    
                    
if __name__ == "__main__":
    
    host = "localhost"
    port = 3316
    user = "root"
    database = "moocdb"
    password = "your password"

    db = MySQLdb.connect(host=host, port=port, user=user, db=database,passwd=password)
    cursor = db.cursor()

    problemList = [330]
    min_time = 10
    certified = False
                        
    generate_csv_file_by_problem( cursor, problemList, min_time, certified)

    db.close()
                                 
    
 

    
