'''
Takes around 1 hour to run.

This script populates the submissions table with attempts number recomputed for the MOOCdb database. 
Running time with 6.002x Fall 2012 data:  seconds

Pre-requisites: 
   
1. You must install the MySQL connector for Python:
   http://sourceforge.net/projects/mysql-python/
   Straightforward to install in Windows 
   (just launch MySQL-python-1.2.4b4.win32-py2.7.exe)
   MySQLdb for Unix: installation instructions:
   http://www.tutorialspoint.com/python/python_database_access.htm
   
2. The users and problems table must have been computed first

3. To optimize the query on the browser logs (will take forever otherwise):

ALTER TABLE `logs`.`br_logs4` DROP COLUMN `filenum` , DROP COLUMN `session` , DROP COLUMN `agent` , DROP COLUMN `event_source` 
, ADD INDEX `username_event_idx` (`username` ASC, `event`(30) ASC) ;


Created on Jun 19, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb 

# http://stackoverflow.com/questions/2835559/python-parsing-file-json
import json

import copy

# Global variables
username_id_mapping = {}
problems_id_name_mapping = {}

def retrieve_username_id_mapping(connection):
    username_id_mapping = {}
    cursor = connection.cursor()
    sql = "SELECT user_id, user_name FROM moocdb.users;"
    cursor.execute(sql)
    
    for i in range(cursor.rowcount):  
        row = cursor.fetchone()
        username_id_mapping[str(row[1])] = row[0]
    
    return username_id_mapping

def retrieve_problems_id_name_mapping(connection):
    problems_id_name_mapping = {}
    cursor = connection.cursor()
    sql = "SELECT problem_id, problem_name FROM moocdb.problems;"
    cursor.execute(sql)
    
    for i in range(cursor.rowcount):  
        row = cursor.fetchone()
        problems_id_name_mapping[row[1]] = row[0]
    
    return problems_id_name_mapping

def retrieve_problem_id_assessment_grade_mapping(connection, user_id):    
    problem_id_assessment_grade_mapping = {}
    cursor = connection.cursor()
    
    sql = '''
    SELECT submissions.problem_id,  assessments.assessment_grade
    FROM moocdb.submissions AS submissions, moocdb.assessments AS assessments
    WHERE submissions.submission_id = assessments.submission_id
    AND submissions.user_id = %s;
    ''' % user_id
    cursor.execute(sql)
    
    for i in range(cursor.rowcount):  
        row = cursor.fetchone()
        problem_id_assessment_grade_mapping[row[0]] = row[1]
    
    return problem_id_assessment_grade_mapping    

def clear_submissions(connection):
    '''
    This function empties the submissions table.
    
    To solve the issue "(1701, 'Cannot truncate a table referenced in a foreign key constraint":
    http://stackoverflow.com/a/8074510/395857
    '''
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute("TRUNCATE moocdb.submissions2;")
    cursor.execute("ALTER TABLE moocdb.submissions2 AUTO_INCREMENT = 1;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    connection.commit()
    
def retrieve_usernames(connection):
    '''
    Retrieve all usernames that have made at least one submission
    '''
    
    cursor = connection.cursor()    
    sql = '''
    SELECT DISTINCT(username) FROM logs2.srv_logs 
    WHERE USERNAME <> ""
        AND event_type LIKE "/modx/problem/filename%/problem_get"
    LIMIT 100;
    '''
    cursor.execute(sql)
    usernames = list()
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        usernames.append(row[0])
        
    #print usernames
    return usernames

def insert_br_logs_problem_id(connection):
    '''
    
    '''
    # Hardcoded 15 because we only have around 11 000 000 rows in br_logs4:  SELECT  COUNT(*)  FROM logs.br_logs4;
    for i in range (15):
        print "\nStep " + str(i) + " out of 15."
        insert_br_logs_problem_id_offset(connection, 1000000, 1000000 * i)
    
    print "insert_br_logs_problem_id is done!"
    cursor = connection.cursor()
    cursor.execute("SELECT  COUNT(*)  FROM logs.br_logs4 WHERE problem_id IS NULL;")
    row = cursor.fetchone()
    print "Number of rows with NULL as problem_id: " + str(row[0]) + " (it should be 0)"
    
def insert_br_logs_problem_id_offset(connection, limit, offset):
    '''
    
    '''
    
    global username_id_mapping, problems_id_name_mapping
    
    cursor = connection.cursor()
    # Note the ORDER BY UNIX_TIMESTAMP(time) ASC! we need to order by time so that we correctly order the attempt number
    # Also, we need UNIX_TIMESTAMP otherwise the ordering will be messed up
    
    print "Retrieving the browser logs"
    sql = '''
    SELECT id, event FROM logs.br_logs4
    -- ORDER BY id ASC
    LIMIT %s
    OFFSET %s
    '''% (limit, offset)
      
    record_list = list()
    cursor.execute(sql)
    print "ok"
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        #print row
        
        if (row[1].find("\"input_filename") != -1):        
            submissions = row[1].split(",\"input_filename")
        elif (row[1].find("input_filename") != -1):
            submissions = row[1].split(",input_filename")
        else:
            print "Couldn't get the get all the submissions"
            assert(False)
            
        submission = submissions[0]
        submission = submission.replace("}", "")
        submission = submission.replace("{", "")
        submission = submission.replace("\"", "")
            
        submission = submission.replace("input_filename", "filename")
        #print submission
        separation = submission.find(":")
        problem = submission[0:separation]
        #print problem 
        problem_id = problems_id_name_mapping[problem]
        #print problem_id
        
        record = list()        
        record.append(str(problem_id))
        record.append(str(row[0]))
        #print record
        record_list.append(record)
        
        if i % 10000 == 0:
            print "Progress: " + str(float(i) / cursor.rowcount * 100) + "%"
            
    
    # Update br_logs 
    #print record_list
    print "Updating the browser logs"
    sql_update_br_logs= '''\
                        UPDATE logs.br_logs4
                        SET problem_id = %s
                        WHERE id = %s
             
           ''' 
    cursor.executemany(sql_update_br_logs, record_list)
     
    connection.commit()
    
    
def find_submissions(connection, username):
    '''
    
    '''
    # We don't care about anonymous people
    if not username:
        return
    
    global username_id_mapping, problems_id_name_mapping
    
    cursor = connection.cursor()
    # Note the ORDER BY UNIX_TIMESTAMP(time) ASC! we need to order by time so that we correctly order the attempt number
    # Also, we need UNIX_TIMESTAMP otherwise the ordering will be messed up
    sql = '''
    SELECT time, event FROM logs.br_logs4
    WHERE event_type = 10 AND username = '%s'
    ORDER BY event ASC, UNIX_TIMESTAMP(time) ASC
    LIMIT 1000000;
    ''' % username
    
    cursor.execute(sql)
    mydecoder = json.JSONDecoder()
    print username + " has " + str(cursor.rowcount) + " events."
    previous_problem = ""
    previous_answers = list()  # Map problem names and number of attempts
    attempt_numbers = list()
    previous_attempt_numbers = list()
    record_submission_list = list()
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        print row
        #data = mydecoder.decode(row[1])
        
        # First we get all the submissions and create problems and answers list
        
        if (row[1].find("\"input_filename") != -1):        
            submissions = row[1].split(",\"input_filename")
        elif (row[1].find("input_filename") != -1):
            submissions = row[1].split(",input_filename")
        else:
            print "Couldn't get the get all the submissions"
            assert(False)
            
        count = 0
        problems = list()
        answers = list()
        
        
        #print row[1].find(",\"input_filename")
        #assert(row[1].find(",\"input_filename") != -1)
        
        for submission in submissions:
            count += 1
            submission = submission.replace("}", "")
            submission = submission.replace("{", "")
            submission = submission.replace("\"", "")
            
            submission = submission.replace("input_filename", "")
            print submission
            #print len(submissions)  
            separation = submission.find(":")
            problem = submission[0:separation]
            answer = submission[separation+1:]
            problems.append(problem)
            answers.append(answer)
            #print problem
            #print answer
               
        changed = [False for i in range(len(submissions))]
         
        #print submissions
        # Check if this is a new problem - we just need to check it for the first submission in the record
        #print "previous_problem: " +previous_problem
        #print "problems[0]: " +problems[0]
        if previous_problem != problems[0]:
            previous_problem = problems[0]            
            attempt_numbers = list()
            previous_attempt_numbers = [0 for i in range(len(submissions))]
            for submission_number in range(len(submissions)):
                #previous_answers[problems[submission_number]] = answers[submission_number]
                previous_answers.append(answers[submission_number])
                # If the first answer is empty, we don't count it as an attempt
                # http://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
                if not answers[submission_number]:
                    attempt_numbers.append(0)
                else:
                    attempt_numbers.append(1)
                            
        # If this is not a new problem, increment the number of the attempts if the answer is different        
        else:
            for submission_number in range(len(submissions)):
                #print "submission_number: " + str(submission_number)
                #print answers[submission_number] 
                #print previous_answers[submission_number]
                
                # If no answer, we don't count this as an attempt
                if not answers[submission_number]:                    
                    continue
                # increment the number of the attempts if the answer is different
                if answers[submission_number] != previous_answers[submission_number]:
                    attempt_numbers[submission_number] += 1
                    previous_answers[submission_number] = answers[submission_number]
        
        #print "changed: "+ str(changed)
        for submission_number in range(len(submissions)):
            changed[submission_number] = (attempt_numbers[submission_number] != previous_attempt_numbers[submission_number])
        previous_attempt_numbers = copy.deepcopy(attempt_numbers) 
            
        print "attempt_numbers:" + str(attempt_numbers)
        print "changed: "+ str(changed)
        
        # Create new records 
        for submission_number in range(len(submissions)):
            
            # Only create new record if the answer has changed
            if not changed[submission_number]:
                continue
            
            record_submission = list()
            # user_id
            # username
            record_submission.append(username_id_mapping[str(username)])
            
            # problem_id
            record_submission.append(problems_id_name_mapping["filename"+problems[submission_number]])
            
            # submission_timestamp
            record_submission.append(row[0])
            
            # submission_attempt_number
            record_submission.append(attempt_numbers[submission_number])
            
            # submission_answer
            record_submission.append(answers[submission_number])
            
            record_submission_list.append(record_submission)
            
         
    sql_insert_submissions = '''\
                        INSERT INTO moocdb.submissions2 (user_id, problem_id, submission_timestamp, submission_attempt_number, submission_answer)
                        VALUES (%s, %s, %s, %s, %s)
                        ''' 
    cursor.executemany(sql_insert_submissions, record_submission_list)
    
    
    # Now we populate the assessments table
    problem_id_assessment_grade_mapping = retrieve_problem_id_assessment_grade_mapping(connection, 14)
    print problem_id_assessment_grade_mapping
    
    record_assessment_list = []
    
    
    connection.commit()
    
                

def main():
    '''
    This is the main function
    '''
    global username_id, problems_id_name_mapping
    
    connection = mdb.connect('127.0.0.1', 'root', 'database_password', 'moocdb') #, charset='utf8', use_unicode=True);
    #clear_submissions(connection)
    username_id_mapping = retrieve_username_id_mapping(connection)
    problems_id_name_mapping = retrieve_problems_id_name_mapping(connection)
    
    insert_br_logs_problem_id(connection)
    
    connection.close()
    

if __name__ == "__main__":
    main()
