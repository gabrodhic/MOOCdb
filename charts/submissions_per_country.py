'''
-- Takes  seconds to execute   
Created on Jun 27, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import google_charts_wrapper

def main():
    '''
    This function plots the Average number of submissions per country (countries with less than 50 students were removed)
    '''    

    data_sql = '''
    -- Takes 1 seconds to execute
    SELECT users.user_country, (COUNT(*) / countries.country_number_of_users) AS average
    FROM moocdb.submissions AS submissions, moocdb.users AS users, moocdb.countries AS countries
    WHERE submissions.user_id = users.user_id
        AND users.user_country = countries.country_code
        AND countries.country_number_of_users > 50
    GROUP BY users.user_country
    ORDER BY average DESC
    ;

    ;
    '''
    
    options = google_charts_wrapper.options()
    options.set_data(google_charts_wrapper.get_data(data_sql))
    options.set_chart_type("geo_map")   
    options.set_chart_title("Average number of submissions per country (countries with less than 50 students were removed)")
    options.set_height(600)
    options.set_width(1000)
    options.set_page_title("Average number of submissions per country (countries with less than 50 students were removed)")
    options.set_output_file("./output/submissions_per_country.html")
    print options.get_data()
    google_charts_wrapper.generate_html(options)  

if __name__ == "__main__":
    main()
    
