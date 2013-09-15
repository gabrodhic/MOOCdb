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
    This function plots the distribution of the days between the last submission and the deadline
    '''    

    sql = '''
    -- Takes  seconds to execute    
    SELECT 
           FLOOR((UNIX_TIMESTAMP(problems.problem_hard_deadline) 
                - UNIX_TIMESTAMP(submissions.submission_timestamp)) / (3600 * 24 )) AS day,
         COUNT(*) AS `Number of days between the last submission and the deadline for all lecture quizzes`
    FROM moocdb.submissions AS submissions
     INNER JOIN moocdb.problems AS problems
     ON problems.problem_id = submissions.problem_id
    WHERE submissions.submission_attempt_number = ( -- We just want the last attempt
                SELECT MAX(submissions2.submission_attempt_number)
                FROM moocdb.submissions AS submissions2
                WHERE submissions2.problem_id = submissions.problem_id
                    AND submissions2.user_id = submissions.user_id
            )
        AND problems.problem_type_id = 2 -- = 2 means lecture quizzes
     GROUP BY day
     ORDER BY day ASC 
    ;
    ;
        '''
    
    # Careful, wrapper needs to be fixed: transpose result matrix
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("column_chart")   
    options.set_chart_title("Number of days between the last submission and the deadline for all lecture quizzes")
    options.set_height(500)
    options.set_width(1200)
    options.set_page_title("Number of days between the last submission and the deadline for all lecture quizzes")
    options.set_h_axis("{title: 'Day #' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of submissions',  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/days_last_submission_before_deadline_lecture_quizzes.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
