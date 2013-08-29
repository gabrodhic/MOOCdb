'''
Created on Jun 25, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the number of edits on the wiki every day from 2012-03-04
    '''    

    sql = '''
    -- Takes 10 seconds to execute
    SELECT wiki.day, `Number of edits on the wiki`, `Number of posts on the forum`
    FROM (
        -- Takes 5 seconds to execute
        SELECT CONCAT(CAST( collaborations.collaboration_timestamp AS DATE) , '') AS day, COUNT(*) AS `Number of edits on the wiki`
        FROM moocdb.collaborations AS collaborations
        WHERE collaborations.collaboration_parent_id = 2
        GROUP BY day
        ORDER BY day ASC
    ) wiki,
        (-- Takes 5 seconds to execute
        SELECT CONCAT(CAST(collaborations.collaboration_timestamp AS DATE), '') AS day, COUNT(*) AS `Number of posts on the forum`
        FROM moocdb.collaborations AS collaborations
        WHERE collaborations.collaboration_parent_id = 1
        GROUP BY day
        ORDER BY day ASC
    ) forum
    WHERE forum.day = wiki.day
    
    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(sql))
    options.set_chart_type("area_chart")   
    options.set_chart_title("Number of edits on the wiki and posts on the forum by date")
    options.set_height(500)
    options.set_width(900)
    options.set_page_title("Number of edits on the wiki and posts on the forum by date")
    options.set_h_axis("{title: 'Date' ,  titleTextStyle: {color: 'blue'}}")
    options.set_v_axis("{title: 'Number of edits on wiki and posts on forum' ,  titleTextStyle: {color: 'blue'}}")
    options.set_output_file("./output/wiki_edits_and_forum_posts_per_day_date_label.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
