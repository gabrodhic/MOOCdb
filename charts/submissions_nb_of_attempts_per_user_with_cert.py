'''
-- Takes 5 seconds to run
Created on Jun 27, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of submissions per user who got a certificate
    '''    

    sql = '''
    -- Takes 5 seconds to run
    -- http://stackoverflow.com/questions/5351628/how-can-i-add-a-new-column-which-counts-the-number-of-rows-as-serial-number
    SELECT @n := @n + 1 `User #`,  t.*
    FROM (SELECT @n:=0) initvars, 
        ( SELECT COUNT(*) AS `Number of submissions` 
            FROM moocdb.submissions AS submissions,
                moocdb.users AS users
            WHERE users.user_final_grade >= 0.5
                AND users.user_id = submissions.user_id
            GROUP BY submissions.user_id 
            ORDER BY `Number of submissions` DESC
        ) t
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("line_chart")   
    options.set_chart_title("Number of submissions per student who got a certificate")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Number of submissions per student who got a certificate")
    options.set_h_axis("{title: 'Student #' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of submissions' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/submissions_nb_of_attempts_per_user_with_cert.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
