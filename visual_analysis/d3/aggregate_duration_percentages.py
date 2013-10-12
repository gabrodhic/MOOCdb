# Created on Oct 3rd, 2013
# Refactored on Oct 11, 2013
# @author: Sherwin Wu for ALFA, MIT lab: sherwu@mit.edu
# @author: Colin Taylor, colin_t@mit.edu
# =============================
# IMPORTANT!!!
# This script requires a file called 'duration_by_user_grade.csv'
# and will output a file called 'duration_aggregate_by_grade.csv'
# =============================
import json
import csv

def initialize_dict(types):
	temp_dict = {}
	for type1 in types:
		temp_dict[type1] = 0
	return temp_dict

if __name__ == "__main__":
	in_csv = open('duration_by_user_grade.csv')
	csv_reader = csv.DictReader(in_csv)
	grades = ['A', 'B', 'C']

	fields = csv_reader.fieldnames
	assert('grade' == fields[1])
	assert('country' == fields[2])
	resource_types = fields[3:] #get the resource type names from the input csv

	header = ['grade'] + resource_types
	out_csv = open('duration_aggregate_by_grade.csv', 'wb')
	csv_writer = csv.DictWriter(out_csv, delimiter= ',', fieldnames= header)
	csv_writer.writeheader()


	grade_counts = initialize_dict(grades)
	grade_resources = {}
	for grade in grades:
		grade_resources[grade] = initialize_dict(resource_types)

	#sum up the durations for each grade and resource_type
	for row in csv_reader:
		grade = row['grade']
		resources_dict = grade_resources[grade] #pick the resources_dict by the grade of the user
		for resource_type in resource_types:
			value = float(row[resource_type])
			resources_dict[resource_type] += value #add the value of each resource type to the total
		grade_counts[grade] += 1

	# write the duration for each grade
	for grade in grades:
		resources_dict = grade_resources[grade] #pick the resources_dict by the grade of the user
		grade_count = grade_counts[grade]
		for resource_type in resource_types:
			resources_dict[resource_type] /= grade_count
		resources_dict['grade'] = grade
		csv_writer.writerow(resources_dict)

	out_csv.close()
	in_csv.close()

