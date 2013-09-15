'''
Takes 900he seconds to execute
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
    -- duration_per_grade.sql
    -- Takes 900 seconds to execute
    SELECT letter_grade.grade,
        (COUNT(*) / letter_grade.number_of_students) AS occurrences,
        MIN(observed_events.observed_event_duration),
        MAX(observed_events.observed_event_duration),
        AVG(observed_events.observed_event_duration),
        STD(observed_events.observed_event_duration),
        SUM(observed_events.observed_event_duration) / letter_grade.number_of_students
        
    FROM moocdb.observed_events AS observed_events,
         moocdb.users AS users,
        moocdb.letter_grade AS letter_grade
    WHERE observed_events.user_id = users.user_id
        AND letter_grade.grade = users.user_final_grade
    GROUP BY letter_grade.grade
    ORDER BY SUM(observed_events.observed_event_duration) DESC
    ;

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
    
