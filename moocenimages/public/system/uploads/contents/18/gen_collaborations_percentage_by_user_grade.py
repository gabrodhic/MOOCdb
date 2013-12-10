# Created on Oct 9th, 2013
# @author: Sherwin Wu for ALFA, MIT lab: sherwu@mit.edu
# =============================
# IMPORTANT!!!
# =============================

import moocdb_tools as mt
import json

if __name__ == "__main__":
    collab_by_grade_csv = open('collaborations_percentage_by_user_grade.csv', 'wb') 
    collab_by_grade_csv_writer = csv.DictWriter(collab_by_grade_csv, delimiter=',', \
        field_names=['user_grade', 'forum_question', 'forum_answer', 'forum_comment', 'wiki_revision'])
    collab_by_grade_csv_writer.writeheader()

    # a dictionary of user_ids to the grade they received
    user_id_to_grade = {}

    # a list of the possible user grades
    possible_user_grades = ['A', 'B', 'C', 'else']

    # a dictionary counting the number of A, B, C, and else students
    student_grade_count = mt.counter_dict(possible_user_grades)

    collaboration_types = ['forum_question', 'forum_answer', 'forum_comment', 'wiki_revision']
    collaboration_type_id_to_name = {1: 'forum_question', 2: 'forum_answer', 3: 'forum_comment', 4: 'wiki_revision'}

    A_dict = mt.counter_dict(collaboration_types)
    B_dict = mt.counter_dict(collaboration_types)
    C_dict = mt.counter_dict(collaboration_types)
    else_dict = mt.counter_dict(collaboration_types)
    students_collaboration_count_dict = {'A': A_dict, 'B': B_dict, 'C': C_dict, 'else': else_dict}
    for i in range(cursor.rowcount):
        [user_id, collaboration_type_id] = cursor.fetchone()

        grade = user_id_to_grade[user_id] if user_id in user_id_to_grade else 'else'
        collaboration_type_name = collaboration_type_id_to_name[collaboration_type_id]

        students_collaboration_count_dict[grade][collaboration_type_name] += 1

        
    for grade in possible_user_grades:
        collab_by_grade_csv_writer.writerow(
            # this takes the dictionary stored in students_collaboration_count_dict
            # and adds a 'user_grade': GRADE entry to it.
            dict(students_collaboration_count_dict[grade].items() + [('user_grade', grade)])
        )
  

    collab_by_grade_csv.close()
