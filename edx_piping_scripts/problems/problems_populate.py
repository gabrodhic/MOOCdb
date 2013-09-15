'''
This script populates the problems table for the MOOCdb database. 
Running time with 6.002x Fall 2012 data: 150 seconds

Pre-requisites: 
1. The field problem_name should be not enough (e.g VARCHAR(60))
   otherwise it will trigger an error message such as:
   "Warning: Data truncated for column 'problem_name' at row 1"
   
2. You must have run problem_types_populate_with_0.sql or populate 
   the problem_types table with at least a row with problem_type_id = 0
   otherwise it will trigger an error message such as:
   "Mysql error 1452 - Cannot add or update a child row: a foreign key constraint fails"
   
3. You must install the MySQL connector for Python:
   http://sourceforge.net/projects/mysql-python/
   Straightforward to install in Windows 
   (just launch MySQL-python-1.2.4b4.win32-py2.7.exe)
   MySQLdb for Unix: installation instructions:
   http://www.tutorialspoint.com/python/python_database_access.htm

   
Created on Jun 10, 2013
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


connection = mdb.connect('127.0.0.1', 'root', 'database_password', 'moocdb');
cursor = connection.cursor()

'''
This SQL query should return 1,555,985 rows, as you can see by executing:
SELECT count(*) FROM forum_data.courseware_studentmodule
WHERE module_type = 'problem'
AND state IS NOT NULL
AND state NOT LIKE '%attempts": 0%';
'''

sql = '''\
    SELECT state FROM forum_data.courseware_studentmodule 
    WHERE module_type = 'problem' 
    AND state IS NOT NULL 
    AND state NOT LIKE '%attempts\": 0%' 
    ORDER BY created ASC 
    LIMIT 100000000;
    '''
    
cursor.execute(sql)

problem_set = set()
mydecoder = json.JSONDecoder()
for i in range(cursor.rowcount):        
        row = cursor.fetchone()
        #print row
        #print row[0]
        
        data = mydecoder.decode(row[0])
        #print data
        #print data["student_answers"]
        for k in data["student_answers"].keys():
            #print k
            problem_set.add(k)
        
#print sorted(problem_set)
print problem_set
print str(len(problem_set)) + " rows should be added in moocdb.problems"

#for problem in problem_set:
sql = '''\
    INSERT INTO moocdb.problems (problem_name, problem_type_id)
    VALUES (%s, 0)
    '''
cursor.executemany(sql, problem_set)

connection.commit()
connection.close()
