'''
This script populates the submissions table for the MOOCdb database. 
Running time with 6.002x Fall 2012 data: 300 seconds

Pre-requisites: 
   
1. You must install the MySQL connector for Python:
   http://sourceforge.net/projects/mysql-python/
   Straightforward to install in Windows 
   (just launch MySQL-python-1.2.4b4.win32-py2.7.exe)
   MySQLdb for Unix: installation instructions:
   http://www.tutorialspoint.com/python/python_database_access.htm
   
2. The problems table must have been compulated first

Created on Jun 11, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb 

# http://stackoverflow.com/questions/2835559/python-parsing-file-json
import json


def retrieve_problems_id_name_mapping(connection):
    problems_id_name_mapping = {}
    cursor = connection.cursor()
    sql = "SELECT problem_id, problem_name FROM moocdb.problems;"
    cursor.execute(sql)
    
    for i in range(cursor.rowcount):  
        row = cursor.fetchone()
        problems_id_name_mapping[row[1]] = row[0]
    
    return problems_id_name_mapping




def clear_submissions(connection):
    '''
    This function empties the submissions table.
    
    To solve the issue "(1701, 'Cannot truncate a table referenced in a foreign key constraint":
    http://stackoverflow.com/a/8074510/395857
    '''
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute("TRUNCATE moocdb.submissions;")
    cursor.execute("ALTER TABLE moocdb.submissions AUTO_INCREMENT = 1;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    connection.commit()
    
    
def clear_assessments(connection):
    '''
    This function empties the assessments table.
    
    To solve the issue "(1701, 'Cannot truncate a table referenced in a foreign key constraint":
    http://stackoverflow.com/a/8074510/395857
    '''
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute("TRUNCATE moocdb.assessments;")
    cursor.execute("ALTER TABLE moocdb.assessments AUTO_INCREMENT = 1;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    connection.commit()

def insert_submissions(connection):

    problems_id_name_mapping = retrieve_problems_id_name_mapping(connection)
    
    '''
    This SQL query should return 1,555,985 rows, as you can see by executing:
    SELECT count(*) FROM forum_data.courseware_studentmodule
    WHERE module_type = 'problem'
    AND state IS NOT NULL
    AND state NOT LIKE '%attempts": 0%';
    '''
    
    sql = '''\
        SELECT state, student_id, created FROM forum_data.courseware_studentmodule 
        WHERE module_type = 'problem' 
        AND state IS NOT NULL 
        AND state NOT LIKE '%attempts\": 0%' 
        ORDER BY created ASC 
        LIMIT 100000000;
        '''
    
    cursor = connection.cursor()    
    cursor.execute(sql)
    
    problem_name_list = list()
    user_id_list = list()
    submission_timestamp_list = list()
    submission_answer_list = list()
    record_list = list()
    record_assessment_list = list()
    #grader_id_list = list()
    submission_id = 1
    no_pb_in_correct_map = 0
    
    mydecoder = json.JSONDecoder()
    for i in range(cursor.rowcount):        
            row = cursor.fetchone()
            #print row
            #print row[0]
            
            
            data = mydecoder.decode(row[0])
            
            '''
            print data
            print data["student_answers"]
            print data["correct_map"]
            print 
            print row[1]
            print row[2]
            '''
            for key, value in data["student_answers"].iteritems():
                
                ## Create new record for the submissions table
                # create new record
                record = list()
                
                # user_id
                record.append(int(row[1]))
                
                # problem_id
                record.append(problems_id_name_mapping[key])
                
                # submission_timestamp
                record.append(row[2])
                
                # submission_attempt_number
                record.append(data["attempts"])
                
                # submission_answer
                #record.append("a")
                # http://stackoverflow.com/questions/2365411/python-convert-unicode-to-ascii-without-errors
                record.append(value.encode('ascii', 'ignore'))
                
                # grader_id
                record.append(1)
            
                # Add new record to record list
                record_list.append(tuple(record))
                # print record_list
                
                ## Create new record for the assessments  table
                # create new assessment record
                record_assessment = list()
                
                # submission_id
                record_assessment.append(submission_id)
                
                # assessment_feedback
                record_assessment.append("")
                
                # assessment_grade                
                if (key in data["correct_map"]) and (data["correct_map"][key] == "correct"):
                    record_assessment.append(1)
                else:
                    record_assessment.append(0)
                
                if key not in data["correct_map"]:
                    no_pb_in_correct_map += 1
                    no_pb_in_correct_map_data = data
                
                # assessment_grader_id
                record_assessment.append(1)
                
                # assessment_timestamp
                record_assessment.append(row[2])
                
                record_assessment_list.append(record_assessment)
                
                submission_id += 1
            
                if submission_id % 10000 == 0:
                    cursor2 = connection.cursor()
                    print "Percent done: " + str(float(i) / cursor.rowcount * 100) + "%"
                    print str(len(record_list)) + " rows should be added in moocdb.problems"
                    
                    # for problem in problem_set:
                    # http://stackoverflow.com/questions/2623418/how-do-i-insert-data-from-a-python-dictionary-to-mysql    
                    # sql2 = '''\
                    #    INSERT INTO moocdb.submissions (user_id, problem_id, submission_answer, grader_id)
                    #    VALUES (12, 1, 'a', 1)
                    #    '''
                        
                    sql = '''\
                        INSERT INTO moocdb.submissions (user_id, problem_id, submission_timestamp, submission_attempt_number, submission_answer, grader_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                    
                    sql_assessment = '''\
                        INSERT INTO moocdb.assessments (submission_id, assessment_feedback, assessment_grade, assessment_grader_id, assessment_timestamp)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                    
                    # http://dev.mysql.com/doc/connector-python/en/myconnpy_MySQLCursor_executemany.html
                    # The executemany() iterates through the sequence of parameters calling the execute() method. 
                    # Inserting data, however, is optimized by batching them using multipler-row syntax.
                    #print "record_list:"
                    #record_list = [(12, 1, 'a', 1), (12, 1, 'a', 1)]
                    #print record_list
                    #cursor.execute(sql2)
                    cursor2.executemany(sql, record_list)
                    cursor2.executemany(sql_assessment, record_assessment_list)
                    
                    connection.commit()
                    
                    # Clear lists
                    del record_assessment_list[:]
                    record_assessment_list = list()
                    del record_list[:]
                    record_list = list()
    
    print "no_pb_in_correct_map=" + str(no_pb_in_correct_map)
    print "no_pb_in_correct_map_data=" + str(no_pb_in_correct_map_data)
    
    
def main():
    '''
    This is the main function
    '''
    
    connection = mdb.connect('127.0.0.1', 'root', '', 'moocdb') #, charset='utf8', use_unicode=True);
    clear_assessments(connection)
    clear_submissions(connection)
    insert_submissions(connection)
    
    connection.close()
    

if __name__ == "__main__":
    main()
