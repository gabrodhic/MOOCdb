'''
Takes 5 seconds to execute
Created on Jun 27, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
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
    SELECT @n := @n + 1 `Number of Submissions`,  t.*
    FROM (SELECT @n:=0) initvars, 
        ( SELECT LOG(LENGTH(collaborations.collaboration_content)) AS `Logarithmic length`
        FROM moocdb.collaborations AS collaborations
        WHERE LENGTH(collaborations.collaboration_content) > 0
        ORDER BY LENGTH(collaborations.collaboration_content) DESC 
        ) t;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("line_chart")   
    options.set_chart_title("Distribution of the length of the posts on the forum")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Distribution of the length of the posts on the forum")
    options.set_h_axis("{title: 'Post #' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Length of the post (logarithm)' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/forum_post_length.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
