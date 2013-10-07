# Created on Oct 3rd, 2013
# @author: Sherwin Wu for ALFA, MIT lab: sherwu@mit.edu
# =============================
# IMPORTANT!!!
# This script requires a file called 'percent_duration_by_user_grade.csv'
# and will output a file called 'percent_duration_aggregate.csv'
# =============================
import MySQLdb as mdb
import json

if __name__ == "__main__":
    connection = mdb.connect('127.0.0.1', 'root', 'edx2013', 'moocdb', port=3316, charset='utf8')

    with open('percent_duration_by_user_grade.csv') as f:
        infos = f.readlines()
    del infos[0]
    
    out_csv = open('percent_duration_aggregate.csv', 'wb')
    out_csv.write('grade,book,courseware,exam,homework,info,profile,tutorial,unknown,wiki\n')

    A_count = 0
    B_count = 0
    C_count = 0
    A_resources = {'book':0, 'courseware':0, 'exam':0, 'homework':0, 'info':0, 'profile':0, 'tutorial':0, 'unknown': 0, 'wiki': 0}
    B_resources = {'book':0, 'courseware':0, 'exam':0, 'homework':0, 'info':0, 'profile':0, 'tutorial':0, 'unknown': 0, 'wiki': 0}
    C_resources = {'book':0, 'courseware':0, 'exam':0, 'homework':0, 'info':0, 'profile':0, 'tutorial':0, 'unknown': 0, 'wiki': 0}

    
    for info in infos:
        info = info.replace('\n', '')
        [user_id,grade,country,book,courseware,exam,homework,info,profile,tutorial,unknown,wiki] = info.split(',')
        (book, courseware, exam, homework, info, profile, tutorial, unknown, wiki) = \
               (float(book), float(courseware), float(exam), float(homework), \
                float(inf), float(profile), float(tutorial), float(unknown), \
                float(wiki))
        
        if grade == 'A':
            A_resources['book'] += book
            A_resources['courseware'] += courseware
            A_resources['exam'] += exam
            A_resources['homework'] += homework
            A_resources['info'] += info
            A_resources['profile'] += profile
            A_resources['tutorial'] += tutorial
            A_resources['unknown'] += unknown
            A_resources['wiki'] += wiki
            A_count += 1
        elif grade == 'B':
            B_resources['book'] += book
            B_resources['courseware'] += courseware
            B_resources['exam'] += exam
            B_resources['homework'] += homework
            B_resources['info'] += info
            B_resources['profile'] += profile
            B_resources['tutorial'] += tutorial
            B_resources['unknown'] += unknown
            B_resources['wiki'] += wiki
            B_count += 1
        elif grade == 'C':
            C_resources['book'] += book
            C_resources['courseware'] += courseware
            C_resources['exam'] += exam
            C_resources['homework'] += homework
            C_resources['info'] += info
            C_resources['profile'] += profile
            C_resources['tutorial'] += tutorial
            C_resources['unknown'] += unknown
            C_resources['wiki'] += wiki
            C_count += 1

    for resource_type in A_resources:
        A_resources[resource_type] /= A_count

    for resource_type in B_resources:
        B_resources[resource_type] /= B_count

    for resource_type in C_resources:
        C_resources[resource_type] /= C_count

    out_csv.write('A,'+ \
                    str(A_resources['book'])+','+ \
                    str(A_resources['courseware'])+','+ \
                    str(A_resources['exam'])+','+ \
                    str(A_resources['homework'])+','+ \
                    str(A_resources['info'])+','+ \
                    str(A_resources['profile'])+','+ \
                    str(A_resources['tutorial'])+','+ \
                    str(A_resources['unknown'])+','+ \
                    str(A_resources['wiki'])+'\n')

    out_csv.write('B,'+ \
                    str(B_resources['book'])+','+ \
                    str(B_resources['courseware'])+','+ \
                    str(B_resources['exam'])+','+ \
                    str(B_resources['homework'])+','+ \
                    str(B_resources['info'])+','+ \
                    str(B_resources['profile'])+','+ \
                    str(B_resources['tutorial'])+','+ \
                    str(B_resources['unknown'])+','+ \
                    str(B_resources['wiki'])+'\n')
    
    out_csv.write('C,'+ \
                    str(C_resources['book'])+','+ \
                    str(C_resources['courseware'])+','+ \
                    str(C_resources['exam'])+','+ \
                    str(C_resources['homework'])+','+ \
                    str(C_resources['info'])+','+ \
                    str(C_resources['profile'])+','+ \
                    str(C_resources['tutorial'])+','+ \
                    str(C_resources['unknown'])+','+ \
                    str(C_resources['wiki'])+'\n')

    out_csv.close()
    connection.close()
