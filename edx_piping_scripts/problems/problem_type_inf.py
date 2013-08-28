'''
This script populates the attribute problem_type_id in the problems table for the MOOCdb database. 
Running time with 6.002x Fall 2012 data: around 2 hours

Pre-requisites: 
   
1. You must install the MySQL connector for Python:
   http://sourceforge.net/projects/mysql-python/
   Straightforward to install in Windows 
   (just launch MySQL-python-1.2.4b4.win32-py2.7.exe)
   MySQLdb for Unix: installation instructions:
   http://www.tutorialspoint.com/python/python_database_access.htm
   
2. The problems table must have been computed first

2. The problem_types table must have been populated first

Created on Jun 23, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb 

import time

# Global variables
problems_id_name_mapping = {}
problems_type_name_id_mapping = {}

def create_temp_br_logs(connection):
    
    # Creating
    sql = '''
        -- -----------------------------------------------------
        -- Table `moocdb`.`temp_br_logs`
        -- -----------------------------------------------------
        CREATE TABLE IF NOT EXISTS `moocdb`.`temp_br_logs` (
          `page` TEXT NULL ,
          `event` TEXT NULL 
          )
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = latin1;    
    '''
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    
    # Populating
    sql = '''
        INSERT INTO `moocdb`.`temp_br_logs` (page, event)
        SELECT page, event FROM logs.br_logs
        WHERE event_type = '10';
    '''
    cursor.execute(sql)
    connection.commit()
    
    
def drop_table(connection, database_name, table_name):
    '''
    Drop the table_name. For safety, drop_table() can only drop tables that begin with temp
    '''
    print table_name[:4]
    if table_name[:4] <> 'temp':
        print "For safety, drop_table() can only drop tables that begin with temp"
        assert(False)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE " + database_name + "." + table_name + ";")
    connection.commit()
    
    
def retrieve_problems_id_name_mapping(connection):
    problems_id_name_mapping = {}
    cursor = connection.cursor()
    sql = "SELECT problem_id, problem_name FROM moocdb.problems;"
    cursor.execute(sql)
    
    for i in range(cursor.rowcount):  
        row = cursor.fetchone()
        problems_id_name_mapping[row[1]] = row[0]
    
    return problems_id_name_mapping


def retrieve_problems_type_name_id_mapping(connection):
    problems_type_name_id_mapping = {}
    cursor = connection.cursor()
    sql = "SELECT problem_type_id, problem_type_name FROM moocdb.problem_types;"
    cursor.execute(sql)
    
    for i in range(cursor.rowcount):  
        row = cursor.fetchone()
        problems_type_name_id_mapping[row[1]] = row[0]
    
    return problems_type_name_id_mapping

# Reset problem type field
# UPDATE moocdb.problems SET problem_type_id = 0;

def insert_problem_type(connection, problem_name):
    global problems_id_name_mapping, problems_type_name_id_mapping
    #print problem_name
    # http://stackoverflow.com/questions/10678229/selectively-escape-percent-in-python
    sql = '''
        SELECT LCASE(page) FROM moocdb.temp_br_logs 
        WHERE event LIKE '%%%s%%'
        LIMIT 1;
    ''' % problem_name
    #print sql
    cursor = connection.cursor()
    cursor.execute(sql)
    
    if cursor.rowcount < 1:
        print "Couldn't find any event with " + problem_name
        return
    
    row = cursor.fetchone()
    #print row
    page = str(row[0])
    type_name = "Unknown"
    
    # We infer the type from the page URL
    if page.find("courseware") >=0:
        type_name = 'Lecture quiz'
    
    if (page.find("homework") >=0) or (problem_name.find("HW") >=0):
        type_name = 'Homework' 
    
    if (problem_name.find("Lab") >=0):
        type_name = 'Lab'

    if page.find("midtermformatexamples") >=0:
        type_name = 'Midterm example'
        
    if page.find("midterm_exam") >=0:
        type_name = 'Midterm exam'
        
    if page.find("final_exam") >=0:
        type_name = 'Final exam'
             
    if page.find("sandbox") >=0:
        type_name = 'Sandbox'
        
    print  page + " mean " + type_name,
            
    # We update the problem type
    problem_id = problems_id_name_mapping[problem_name]
    type_id = problems_type_name_id_mapping[type_name]
    sql = '''
        UPDATE moocdb.problems 
        SET problem_type_id = %s
        WHERE problem_name = '%s'
        ;
    ''' % (type_id, problem_name)
    #print sql
    cursor.execute(sql)
    
    
    connection.commit()

def main():
    '''
    This is the main function
    '''
    global problems_id_name_mapping, problems_type_name_id_mapping
    connection = mdb.connect('127.0.0.1', 'root', '', 'moocdb') #, charset='utf8', use_unicode=True);
    
    print "Creating a temporary table"
    #create_temp_br_logs(connection)
    
    print "Inferring the problem type"
    problems_id_name_mapping = retrieve_problems_id_name_mapping(connection)
    problems_type_name_id_mapping = retrieve_problems_type_name_id_mapping(connection)
    print problems_type_name_id_mapping
    
    count = 0
    start = time.time()
    # This loop could be multi-threaded
    for problem_name in problems_id_name_mapping.keys():
        start2 = time.time()
        count += 1
        print "Problem " + str(count) + " out of " + str(len(problems_id_name_mapping)) + " : " + problem_name,
        insert_problem_type(connection, problem_name)
        end = time.time()
        print " (took: " + str(round((end - start2)*1000)) +" ms ; total elapsed time: " +  str(round((end - start)*1)) + " s)"
        #break
    
    print "Deleting temporary table"
    #drop_table(connection, 'moocdb', 'temp_br_logs')
    
    print "Program done"
    
    
    connection.close()
    

if __name__ == "__main__":
    main()
