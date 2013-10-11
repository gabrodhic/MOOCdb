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
from collections import OrderedDict

def initialize_dict(types):
	temp_dict = {}
	for type1 in types:
		temp_dict[type1] = 0
	return temp_dict

if __name__ == "__main__":
	input_csv = csv.DictReader(open('duration_by_user_grade.csv'))
	grades = ['A', 'B', 'C']

	fields = input_csv.fieldnames
	assert('grade' == fields[1])
	assert('country' == fields[2])
	resource_types = fields[3:] #get the resource type names from the input csv

	header = ['grade'] + resource_types
	out_csv = csv.DictWriter(open('duration_aggregate_by_grade.csv', 'wb'), delimiter= ',', fieldnames= header)

	grade_counts = initialize_dict(grades)
	grade_resources = {}
	for grade in grades:
		grade_resources[grade] = initialize_dict(resource_types)

	
	for row in input_csv:
		grade = row['grade']
		resources_dict = grade_resources[grade] #pick the resources_dict by the grade of the user
		for resource_type in resource_types:
			value = float(row[resource_type])
			resources_dict[resource_type] += value #add the value of each resource type to the total
		grade_counts[grade] += 1

	output = []
	for grade in grades:
		resources_dict = grade_resources[grade] #pick the resources_dict by the grade of the user
		grade_count = grade_counts[grade]
		for resource_type in resource_types:
			resources_dict[resource_type] /= grade_count
		resources_dict['grade'] = grade
		output.append(resources_dict)

	out_csv.writeheader()
	for row in output:
		out_csv.writerow(row)
