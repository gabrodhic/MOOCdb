# Created on Oct 3rd, 2013
# @author: Sherwin Wu for ALFA, MIT lab: sherwu@mit.edu
# =============================
# IMPORTANT!!!
# This script requires a file called 'duration_by_resources_type_by_user.csv'
# and will output a file called 'percent_duration_by_user_grade.csv'
# =============================

import MySQLdb as mdb
import json

if __name__ == "__main__":
    connection = mdb.connect('127.0.0.1', '', '', 'moocdb', port=3316, charset='utf8')

    with open('duration_by_resource_type_by_user.csv') as f:
        infos = f.readlines()
    del infos[0]
    
    out_csv = open('percent_duration_by_user_grade.csv', 'wb')
    out_csv.write('user_id,grade,country,book,courseware,exam,homework, \
                    info,profile,tutorial,unknown,wiki\n')

    current_user_id = int(infos[0].split(',')[0])
    resource_to_time = {'book':0, 'courseware':0, 'exam':0, 'homework':0, 'info':0, 'profile':0, \
                        'tutorial':0, 'unknown': 0, 'wiki': 0}
    total_time = 0
    for info in infos:
        info = info.replace('\n', '')
        [user_id,total_duration,final_grade,user_country,resource_name] = info.split(',')
        user_id = int(user_id)
        total_duration = int(total_duration)
        final_grade = float(final_grade)
        if final_grade == 1:
            final_grade = 'A'
        elif final_grade == 0.75:
            final_grade = 'B'
        elif final_grade == 0.5:
            final_grade = 'C'

        if user_id != current_user_id:
            book_ratio = resource_to_time['book']/float(total_time)
            courseware_ratio = resource_to_time['courseware']/float(total_time)
            exam_ratio = resource_to_time['exam']/float(total_time)
            homework_ratio = resource_to_time['homework']/float(total_time)
            info_ratio = resource_to_time['info']/float(total_time)
            profile_ratio = resource_to_time['profile']/float(total_time)
            tutorial_ratio = resource_to_time['tutorial']/float(total_time)
            unknown_ratio = resource_to_time['unknown']/float(total_time)
            wiki_ratio = resource_to_time['wiki']/float(total_time)
            
            out_csv.write(str(current_user_id)+","+final_grade+","+user_country+","+str(book_ratio)+","+str(courseware_ratio)+","+str(exam_ratio)+"," \
                            +str(homework_ratio)+","+str(info_ratio)+","+str(profile_ratio)+","+str(tutorial_ratio)+"," \
                            +str(unknown_ratio)+","+str(wiki_ratio)+"\n")

            resource_to_time = {'book':0, 'courseware':0, 'exam':0, 'homework':0, 'info':0, 'profile':0, 'tutorial':0, 'unknown': 0, 'wiki': 0}
            total_time = 0
            current_user_id = user_id

        resource_to_time[resource_name] = total_duration
        total_time += total_duration
        
    out_csv.close()
    connection.close()
