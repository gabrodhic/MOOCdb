'''
Takes  seconds to execute
Created on Jun 30, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the distribution of the number of dropouts by week
    '''    

    sql = '''
    -- Takes 1 second to execute
    SELECT CONCAT(users.user_dropout_week, '') AS `Week #`, COUNT(*) AS `Number of dropouts`
    FROM moocdb.users
    WHERE users.user_dropout_week IS NOT NULL 
    GROUP BY users.user_dropout_week
    ;
        '''
    
    # Careful, wrapper needs to be fixed: transpose result matrix
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("column_chart")   
    options.set_chart_title("Number of dropouts by week")
    options.set_height(500)
    options.set_width(1200)
    options.set_page_title("Number of dropouts by week")
    options.set_h_axis("{title: 'Week #' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of dropouts',  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/dropout_per_week.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
