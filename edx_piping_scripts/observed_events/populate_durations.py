'''
Created on Jun 13, 2013

@author: Colin for ALFA, MIT lab: colin2328@gmail.com

Modifications:
- 20130614 - franck.dernoncourt@gmail.com
            Commit in batch, add progress bar, optimize query O(n^2) to O(n) 
            Also we need an index on timestamp to speed up:
			ALTER TABLE `moocdb`.`observed_events` 
			ADD INDEX `timestamp_idx` (`observed_event_timestamp` ASC) ;
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb

import datetime

def main():
	start = datetime.datetime.now()

	db=mdb.connect(user="root",passwd="",db="moocdb")
	db2=mdb.connect(user="root",passwd="",db="moocdb")

	cursor = db.cursor()
	cursor2 = db2.cursor()

	#cursor.execute("SELECT observed_event_id, user_id, observed_event_timestamp FROM observed_events ORDER BY observed_event_timestamp ASC LIMIT 100000")
	cursor.execute("SELECT observed_event_id, user_id, observed_event_timestamp FROM observed_events ORDER BY observed_event_timestamp ASC")

	count = 0
	for row in cursor:
		count += 1
		#print count
		timestamp = row[2]
		user_id = row[1]
		primary_key = row[0]
		sql = 'SELECT observed_event_timestamp FROM observed_events WHERE observed_event_timestamp > "%s" AND user_id = "%s" ORDER BY observed_event_timestamp ASC LIMIT 1' % (timestamp, user_id)
		cursor2.execute(sql)
		duration = 0
		for row2 in cursor2:
			duration = (row2[0] - timestamp).total_seconds()
			if (duration > (60*60)):
				duration = 0
				break
			#if (row2[1] == user_id):
			#	break
			
		cursor2.execute("UPDATE observed_events SET observed_event_duration=%s WHERE observed_event_id = %s" % (duration, primary_key))
		
		if count % 100 == 0:
			db2.commit()
			print "Percent done: " + str(float(count) / cursor.rowcount * 100) + "%" + " in " + str((datetime.datetime.now() - start).total_seconds()) + " seconds."

	db.close()
	db2.close()
	diff = (datetime.datetime.now() - start).total_seconds()
	print 'finished in %s seconds' % diff

if __name__ == "__main__":
    main()
