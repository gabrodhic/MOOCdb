'''
This function plots the final grade distribution

Created on Jun 25, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the final grade distribution
    '''    

    sql = '''
    -- Takes 1 second to execute
    SELECT letter_grade.letter AS `Grade`,  COUNT(*) AS `Number of students` 
    FROM moocdb.users AS users, moocdb.letter_grade AS letter_grade
    WHERE users.user_final_grade = letter_grade.grade
    GROUP BY letter_grade.grade
    ORDER BY letter_grade.grade DESC 
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("pie_chart")   
    options.set_chart_title("Final grade distribution")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Final grade distribution")
    options.set_output_file("./output/final_grade_distribution.html")
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
