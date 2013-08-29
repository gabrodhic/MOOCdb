'''
Created on Jun 25, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of new registered students every day from February 13, 2012
    '''    

    sql = '''
    -- Takes 1 second to execute
    SELECT CONCAT(CAST(users.user_join_timestamp AS DATE), '')  AS `Day`, 
     COUNT(*) AS `Number of new registered students`
     FROM moocdb.users AS users
     WHERE users.user_join_timestamp IS NOT NULL
        AND DATEDIFF(users.user_join_timestamp, '2012-02-13 00:00:01') >= 0
     GROUP BY `Day`
    ORDER BY `Day` ASC 
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("area_chart")   
    options.set_chart_title("New registered students by date")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("New registered students by date")
    options.set_h_axis("{title: 'Date' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'New registered students' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/users_join_date_date_labels.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
