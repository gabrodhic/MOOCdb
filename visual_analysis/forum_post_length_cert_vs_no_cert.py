'''
Takes 5 seconds to execute
Created on Jun 27, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the distribution of the length of the posts on the forum
    '''    

    sql = '''
    -- Takes 5 seconds to execute
    SELECT no_cert.`Average length of posts on forum for students who did not get a certificate`,
    with_cert.`Average length of posts on forum for students who got a certificate`

    FROM
    (SELECT AVG(LENGTH(collaborations.collaboration_content)) AS `Average length of posts on forum for students who did not get a certificate`
        FROM moocdb.collaborations AS collaborations,
             moocdb.users AS users
        WHERE LENGTH(collaborations.collaboration_content) > 0
            AND collaborations.collaboration_parent_id = 1
            AND (users.user_final_grade IS NULL OR users.user_final_grade < 0.5)
            AND users.user_id = collaborations.user_id) no_cert,

    (SELECT AVG(LENGTH(collaborations.collaboration_content)) AS `Average length of posts on forum for students who got a certificate`
            FROM moocdb.collaborations AS collaborations,
                 moocdb.users AS users
            WHERE LENGTH(collaborations.collaboration_content) > 0
                AND collaborations.collaboration_parent_id = 1
                AND users.user_final_grade >= 0.5
                AND users.user_id = collaborations.user_id) with_cert
;
        '''
    
    # Careful, wrapper needs to be fixed: transpose result matrix
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("column_chart")   
    options.set_chart_title("Length of the posts on the forum")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Length of the posts on the forum")
    options.set_h_axis("{title: '' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Average length of the posts',  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/forum_post_length_cert_vs_no_cert.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
