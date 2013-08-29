'''
Created on Jun 27, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of edits on the wiki every day from 2012-03-04
    '''    

    preprocess_sql = '''
    -- Takes 1 seconds to execute    
    -- we first create a temporary table that contains the students of certificates per country
    CREATE OR REPLACE VIEW temp_students_per_country AS
    SELECT users.user_country AS country, COUNT(*) AS count
            FROM moocdb.users AS users
            GROUP BY users.user_country;
    '''
    
    data_sql = '''
    -- 
    SELECT users.user_country, COUNT(*) / temp_students_per_country.count * 100 AS `Percentage of students who got a certificate`
    FROM moocdb.users AS users, temp_students_per_country
    WHERE users.user_final_grade >= 0.5
    AND temp_students_per_country.country = users.user_country
    AND temp_students_per_country.count >= 100
    GROUP BY users.user_country
    ORDER BY count DESC 
    ;
    '''
    
    postprocess_sql = '''
    DROP VIEW temp_students_per_country;    
    ;
    '''
    
    google_charts_wrapper.run_query(preprocess_sql)
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(data_sql))
    options.set_chart_type("geo_map")   
    options.set_chart_title("Percentage of students who got a certificate")
    options.set_height(600)
    options.set_width(1000)
    options.set_page_title("Percentage of students who got a certificate")
    options.set_output_file("./output/user_certifcate_per_country_normalized_cutoff100.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  
    google_charts_wrapper.run_query(postprocess_sql)

if __name__ == "__main__":
    main()
    
