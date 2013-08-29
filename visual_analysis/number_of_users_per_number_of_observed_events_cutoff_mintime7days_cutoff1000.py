'''
Created on Jun 25, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of students per number of observed events
    '''    

    sql = '''
    -- Takes 3600 seconds to execute
    SELECT number_of_events_per_user.`Number of observed events`, COUNT(*) AS `Number of students`
    FROM 
        (
        SELECT COUNT(*) AS `Number of observed events`, observed_events.user_id,
            MIN(observed_events.observed_event_timestamp) AS first_event,
            MAX(observed_events.observed_event_timestamp) AS last_event
        FROM moocdb.observed_events AS observed_events
        GROUP BY observed_events.user_id
        ) number_of_events_per_user
    WHERE DATEDIFF(last_event, first_event) >= 7 
        AND number_of_events_per_user.`Number of observed events` < 1000
    GROUP BY number_of_events_per_user.`Number of observed events`
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("area_chart")   
    options.set_chart_title("Number of students per number of observed events for students having dropped out at least one week after their first event - Cutoff 1000")
    options.set_height(500)
    options.set_width(1200)
    options.set_page_title("Number of students per number of observed events for students having dropped out at least one week after their first event - Cutoff 1000")
    options.set_h_axis("{title: 'Number of observed events' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of students' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/number_of_users_per_number_of_observed_events_cutoff_mintime7days_cutoff1000.html")
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
