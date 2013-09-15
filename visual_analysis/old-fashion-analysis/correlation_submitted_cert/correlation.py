'''
Created on July 02, 2013

@author: Colin for ALFA, MIT lab: colin2328@gmail.com

- Modification 20130703 Franck Dernoncourt - franck.dernoncourt@gmail.com
		- Fix indices in the for row in curso loop
		- Converts decimal to float  
        - Close DB

'''
import MySQLdb as mdb
import scipy.stats as stats
import numpy 

def main():
	connection = mdb.connect(user="root",passwd="edx2013",db="moocdb")
	cursor = connection.cursor()

	sql = '''CREATE OR REPLACE VIEW temp_students_per_country AS
	SELECT users.user_country AS country, COUNT(*) AS count
			FROM moocdb.users AS users
			GROUP BY users.user_country;
	'''
	cursor.execute(sql)


	sql = ''' SELECT t1.`Percentage of students who got a certificate`,
		t2.`Average number of submissions per country for students who got a certificate (countries with less than 50 students were removed)`
	FROM (
		SELECT users.user_country AS country, 
			COUNT(*) / temp_students_per_country.count * 100 AS `Percentage of students who got a certificate`
		FROM moocdb.users AS users, temp_students_per_country
		WHERE users.user_final_grade >= 0.5
		AND temp_students_per_country.country = users.user_country
		AND temp_students_per_country.count >= 100
		GROUP BY users.user_country
		ORDER BY count DESC
		) t1,

		(SELECT users.user_country AS country, 
			(COUNT(*) / countries.country_number_of_users) AS `Average number of submissions per country for students who got a certificate (countries with less than 50 students were removed)`
		FROM moocdb.submissions AS submissions, moocdb.users AS users, moocdb.countries AS countries
		WHERE submissions.user_id = users.user_id
			AND users.user_country = countries.country_code
			AND countries.country_number_of_users > 50
			AND users.user_final_grade >= 0.5
		GROUP BY users.user_country
		ORDER BY `Average number of submissions per country for students who got a certificate (countries with less than 50 students were removed)` DESC
		) t2

	WHERE t1.country = t2.country;
	DROP VIEW temp_students_per_country;
	'''

	cursor.execute(sql)
	length = cursor.rowcount
	
	percentage_vec = [0] * length
	submissions_vec = [0] * length

	for i in range(cursor.rowcount):
		row = cursor.fetchone()		
		percentage_vec[i] = float(row[1])
		submissions_vec[i] = float(row[0])

	print "computing correlation"
	print percentage_vec
	print submissions_vec
	
	print stats.pearsonr(numpy.array(percentage_vec), numpy.array(submissions_vec))

	connection.close()   

    

if __name__ == "__main__":
    main()