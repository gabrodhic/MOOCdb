'''
Created on Jun 25, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of observed events every day from 2012-03-04
    '''    

    sql = '''
    -- Takes 160 seconds to execute
     SELECT DATEDIFF(observed_events.observed_event_timestamp, '2012-03-03 00:00:01') AS Day, 
         COUNT(*)  AS `Number of observed events`
         FROM moocdb.observed_events AS observed_events 
         -- WHERE observed_events.observed_event_duration < 200
         GROUP BY day
        ORDER BY day ASC 
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("area_chart")   
    options.set_chart_title("Number of observed events every day from March 3, 2012")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Number of observed events every day from March 3, 2012")
    options.set_h_axis("{title: 'Day #' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of observed events every day' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/observed_events_per_day.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
