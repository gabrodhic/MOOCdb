'''
Created on Jun 25, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of posts on the forum every day from 2012-03-04
    '''    

    # http://dev.mysql.com/doc/refman/5.0/en/cast-functions.html
    # If you use a number in string context, the number automatically is converted to a string 
    # This way x does not blow Google Chart API
    sql = '''
    SELECT user_posts_all.day, `Number of posts on the forum`, `Number of posts on the forum for users with certificate`
    FROM 
        ( -- Takes 5 seconds to execute
        SELECT CONCAT(CAST(collaborations.collaboration_timestamp AS DATE), '') AS day, COUNT(*) AS `Number of posts on the forum`
        FROM moocdb.collaborations AS collaborations
        WHERE collaborations.collaboration_parent_id = 1
            AND DATEDIFF(collaborations.collaboration_timestamp, '2012-03-03 00:00:01') < 120
        GROUP BY day
        ORDER BY day ASC ) user_posts_all,
    
        ( -- Takes 5 seconds to execute
        SELECT CONCAT(CAST(collaborations.collaboration_timestamp AS DATE), '') AS day, COUNT(*) AS `Number of posts on the forum for users with certificate`
        FROM moocdb.collaborations AS collaborations,
             moocdb.users AS users
        WHERE collaborations.collaboration_parent_id = 1
            AND DATEDIFF(collaborations.collaboration_timestamp, '2012-03-03 00:00:01') < 120
            AND users.user_final_grade >= 0.5
            AND users.user_id = collaborations.user_id
        GROUP BY day
        ORDER BY day ASC) user_posts_with_cert
    WHERE user_posts_with_cert.day = user_posts_all.day
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("area_chart")   
    options.set_chart_title("Number of posts on the forum by date")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Number of posts on the forum by date")
    options.set_h_axis("{title: 'Date' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of posts' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/forum_posts_per_day_date_labels_cutoff120_with_and_without_cert.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
