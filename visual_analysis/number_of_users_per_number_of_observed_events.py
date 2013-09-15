'''
This function plots the final grade distribution

Created on Jun 25, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of students per number of observed_events
    '''    

    sql = '''
    -- Takes 32 seconds to execute
    SELECT number_of_events_per_user.`Number of observed events`, COUNT(*) AS `Number of students`
    FROM 
        (
        SELECT COUNT(*) AS `Number of observed events`, observed_events.user_id
        FROM moocdb.observed_events AS observed_events
        GROUP BY observed_events.user_id
        ) number_of_events_per_user
    GROUP BY number_of_events_per_user.`Number of observed events`
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("area_chart")   
    options.set_chart_title("Number of students per number of observed events")
    options.set_height(500)
    options.set_width(1200)
    options.set_page_title("Number of students per number of observed events")
    options.set_h_axis("{title: 'Number of observed events' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of students' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/number_of_users_per_number_of_observed_events.html")
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
