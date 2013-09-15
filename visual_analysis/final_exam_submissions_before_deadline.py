'''
Created on Jun 29, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of submissions per user
    '''    

    sql = '''
    -- Takes 7 seconds to run
    -- http://stackoverflow.com/questions/5351628/how-can-i-add-a-new-column-which-counts-the-number-of-rows-as-serial-number
    SELECT @n := @n + 1 `Submission before deadline`,  t.*
        FROM (SELECT @n:=0) initvars, 
            (
            SELECT -- submissions.submission_timestamp, problems.problem_hard_deadline,
                TIME_TO_SEC(TIMEDIFF(problems.problem_hard_deadline, submissions.submission_timestamp))/3600 AS diff
            FROM moocdb.submissions AS submissions,
                moocdb.problems AS problems,
                moocdb.problem_types AS problem_types,
                moocdb.assessments AS assessments
            WHERE submissions.problem_id = problems.problem_id
                 AND problems.problem_type_id = problem_types.problem_type_id
                 AND problem_types.problem_type_name = 'Final Exam'
                 AND assessments.submission_id = submissions.submission_id
                 AND assessments.assessment_grade = 1
                AND TIME_TO_SEC(TIMEDIFF(problems.problem_hard_deadline, submissions.submission_timestamp))/3600 > 0
             ORDER BY diff ASC 
            -- LIMIT 1000
            ) t
    -- LIMIT 1000
    ;

    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("line_chart")   
    options.set_chart_title("Submission before deadline")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Submission before deadline")
    options.set_h_axis("{title: 'User #' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of submissions' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/final_exam_submissions_before_deadline.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
