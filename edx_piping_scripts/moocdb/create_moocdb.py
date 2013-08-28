'''
Created on Jun 13, 2013

Created on Jun 11, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb 

import datetime, time

def run_sql_file(filename, connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    '''
    start = time.time()
    
    file = open(filename, 'r')
    sql = s = " ".join(file.readlines())
    print "Start executing: " + filename + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql 
    cursor = connection.cursor()
    # sql = "SELECT problem_id, problem_name FROM moocdb.problems;"
    cursor.execute(sql)    
    connection.commit()
    
    end = time.time()
    print "Time elapsed to run the query:"
    print str((end - start)*1000) + ' ms'
    
    

def main():
    '''
    This is the main function
    '''
    
    connection = mdb.connect('127.0.0.1', 'root', '', 'moocdb') #, charset='utf8', use_unicode=True);
    run_sql_file("create_moocdb_demo.sql", connection)    
    connection.close()
    

if __name__ == "__main__":
    main()
