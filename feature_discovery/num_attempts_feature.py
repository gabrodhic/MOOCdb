## time the script takes to run on mock db:  xx seconds
## date:  
## author:  
## email:  
## description of feature:
##
##
## name for feature:
## would you like to be cited, and if so, how?
##

## BOILER PLATE

## download MySQLdb here: http://sourceforge.net/projects/mysql-python/
import MySQLdb as sql
import csv

def main():
    passwd = 'password'  ## put your MySQL password here
    db = 'small_mock'  ## change to 'mock' to test on large mock database

    ## SELECT statement can produce feature entries on its own in three 
    ## columns (user_id, week_id, feature_value), or can retrieve data
    ## to manipulate into feature entries via python in next section
    your_query = 'SELECT '\
        'users.user_id, '\
	'FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) '\
	    '- UNIX_TIMESTAMP("2012-03-05 12:00:00")) / (3600 * 24 * 7)) AS week, '\
	'COUNT(*) FROM small_mock.users AS users '\
            'INNER JOIN small_mock.submissions AS submissions '\
            'ON submissions.user_id = users.user_id '\
            'AND FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) '\
		'- UNIX_TIMESTAMP("2012-03-05 12:00:00")) / (3600 * 24 * 7)) < 16 '\
            'GROUP BY users.user_id, week'

    mockdb = sql.connect('localhost','root',passwd,db)
    c = mockdb.cursor()
    c.execute(your_query)
    sql_rows = c.fetchall()
    c.close()

    ## delete the following line and add python to manipulate the select
    ## data (sql_rows) into feature entries, if necessary, storing the
    ## final results in feature_entries
    feature_entries = sql_rows

    ## edit the following line if you'd like to change where the csv is saved
    results = open('/feature_results_test_attempts.csv', 'w')
    
    writer = csv.writer(results)
    writer.writerow(['user_id', 'week_id', 'feature_value'])
    writer.writerows(feature_entries)
    results.close()
    mockdb.close()

if __name__=="__main__":
    main()