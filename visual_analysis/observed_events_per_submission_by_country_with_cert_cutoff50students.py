'''
-- Takes 1 seconds to execute   
Created on Jun 27, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of observed events per submission by country
    '''    

    data_sql = '''
    -- Takes 1 seconds to execute   
    SELECT users.user_country AS `Country`,
    AVG(users.user_observed_events_count / users.user_submissions_count) AS `Number observed events per submission for students who got a certificate`
    FROM moocdb.users AS users
    WHERE users.user_observed_events_count > 0
        AND users.user_submissions_count > 0
        AND users.user_final_grade >= 0.5
    GROUP BY `Country`
    HAVING COUNT(*) > 50
    ORDER BY `Number observed events per submission for students who got a certificate` DESC
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(data_sql))
    options.set_chart_type("geo_map")   
    options.set_chart_title("Number observed events per submission for students who got a certificate by country having at least 50 students")
    options.set_height(600)
    options.set_width(1000)
    options.set_page_title("Number observed events per submission for students who got a certificate by country having at least 50 students")
    options.set_output_file("./output/observed_events_per_submission_by_country_with_cert_cutoff50students.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
