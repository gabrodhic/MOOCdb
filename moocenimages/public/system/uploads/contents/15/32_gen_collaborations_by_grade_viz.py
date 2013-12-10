# Created on Oct 9th, 2013
# @author: Sherwin Wu for ALFA, MIT lab: sherwu@mit.edu
# =============================
# IMPORTANT!!!
# =============================

import moocdb_tools as mt
import json

if __name__ == "__main__":
    connection = mt.connect_to_moocdb()

    cursor1 = connection.cursor()
    # TODO: finish writing this sql query so that we get
    # results of the form (user_id, grade, country)
    cursor1.execute("""
        SELECT
        """)

    collab_by_grade_csv = open('collaborations_percentage_by_user_grade.csv', 'wb') 
    collab_by_grade_csv_writer = csv.DictWriter(collab_by_grade_csv, delimiter=',', \
        field_names=['user_grade', 'forum_question', 'forum_answer', 'forum_comment', 'wiki_revision'])
    collab_by_grade_csv_writer.writeheader()

    grade_by_collab_csv = open('user_grade_percentage_by_collaboration.csv', 'wb')
    grade_by_collab_csv_writer = csv.DictWriter(collab_by_grade_csv, delimiter=',', \
        field_names=['collaboration_type', 'A', 'B', 'C', 'else'])
    grade_by_collab_csv_writer.writeheader()

    # a dictionary of user_ids to the grade they received
    user_id_to_grade = {}

    # a list of the possible user grades
    possible_user_grades = ['A', 'B', 'C', 'else']

    # a dictionary counting the number of A, B, C, and else students
    student_grade_count = mt.counter_dict(possible_user_grades)

    for i in range(cursor1.rowcount):
        [user_id, grade, country] = cursor.fetchone()
        grade = grade if grade != '' else 'else'
        student_grade_count[grade] += 1
        user_id_to_grade[user_id] = grade

    cursor2 = connection.cursor()
    cursor.execute("""
        SELECT user_id, collaboration_type_id 
        FROM moocdb.collaborations;
        """)

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


    grade_by_collab_csv_writer.writerow(
        dict(student_grade_count.items() + [('collaboration_type', 'students')])
    )
    for collaboration_type in collaboration_types:
        row_dict = {'collaboration_type': collaboration_type}
        for grade in possible_user_grades:
            row_dict[grade] = students_collaboration_count_dict[grade][collaboration_type]
        grade_by_collab_csv_writer.writerow(row_dict)
  

    collab_by_grade_csv.close()
    grade_by_collab_csv.close()
    connection.close()
