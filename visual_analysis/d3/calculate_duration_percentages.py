# Created on Oct 3rd, 2013
# Refactored on Oct 11, 2013
# @author: Sherwin Wu for ALFA, MIT lab: sherwu@mit.edu
# @author: Colin Taylor, colin_t@mit.edu
# =============================
# IMPORTANT!!!
# This script will output a file called 'duration_by_user_grade.csv'
# =============================

import MySQLdb as mdb
import json
import csv

def write_column_to_csv(csv, column):
    csv.write(str(column))
    csv.write(',')

def initialize_dict(resource_types):
    temp_dict = {}
    for resource_type in resource_types:
        temp_dict[resource_type] = 0
    return temp_dict

if __name__ == "__main__":
    connection = mdb.connect('127.0.0.1', '', '', 'moocdb', port=3316, charset='utf8')

    cursor = connectin.cursor()
    cursor.execute("""
        SELECT observed_events.user_id,
            SUM(observed_events.observed_event_duration),
            users.user_final_grade,
            users.user_country,
            resource_types.resource_type_content
        FROM moocdb.observed_events AS observed_events,
            moocdb.users AS users, moocdb.resources_urls AS resources_urls,
            moocdb.resources AS resources, moocdb.resource_types AS resource_types
        WHERE (users.user_final_grade=1 OR users.user_final_grade=2 OR users.user_final_grade=0.5)
            AND users.user_id = observed_events.user_id
            AND resources_urls.url_id = observed_events.url_id
            AND resources.resource_id = resources_urls.resource_id
            AND resource_types.resource_type_id = resources.resource_type_id
        GROUP BY resource_types.resource_type_content;
    """)
    
    out_csv = csv.writer(open('duration_by_user_grade.csv', 'wb'))
    resource_types = ['lecture', 'tutorial', 'informational', 'problem', \
        'exam', 'wiki', 'forum', 'profile', 'index', 'book', 'survey', 'home', \
        'other']

    #write column headers to csv
    write_column_to_csv(out_csv, 'user_id')
    write_column_to_csv(out_csv, 'grade')
    write_column_to_csv(out_csv, 'country')
    for resource_type in resource_types:
        write_column_to_csv(out_csv, resource_type)
    write_column_to_csv(out_csv, '\n')

    current_user_id = None
    resource_to_time = initialize_dict(resource_types)

    total_time = 0
    for i in range(cursor.rowcount):
        (user_id,total_duration,final_grade,user_country,resource_name) = cursor.fetchone()
        user_id = int(user_id)
        total_duration = int(total_duration)
        final_grade = float(final_grade)
        if final_grade == 1:
            final_grade = 'A'
        elif final_grade == 0.75:
            final_grade = 'B'
        elif final_grade == 0.5:
            final_grade = 'C'

        if current_user_id = None:
            current_user_id = user_id

        if user_id != current_user_id:
            ratios = initialize_dict(resource_types)
            for resource_type in resource_types:
                ratios[resource_type] = resource_to_time[resource_type] / float(total_time)

            #write row to csv with the ratios
            write_column_to_csv(out_csv, current_user_id)
            write_column_to_csv(out_csv, final_grade)
            write_column_to_csv(out_csv, user_country)
            for resource_type in resource_types:
                write_column_to_csv(out_csv, ratios[resource_type]
            write_column_to_csv(out_csv, '\n')

            resource_to_time = initialize_dict(resource_types)            
            total_time = 0
            current_user_id = user_id

        resource_to_time[resource_name] = total_duration
        total_time += total_duration
        
    out_csv.close()
    connection.close()
