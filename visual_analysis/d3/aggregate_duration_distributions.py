# Created on Oct 3rd, 2013
# Refactored on Oct 11, 2013 to include grade and country
# @author: Sherwin Wu for ALFA, MIT lab: sherwu@mit.edu
# @author: Colin Taylor, colin_t@mit.edu
# =============================
# IMPORTANT!!!
# This script requires a file called 'duration_by_user_grade.csv'
# and will output a file called 'duration_aggregate_by_grade.csv' and 'duration_aggregate_by_country.csv'
# =============================
import json
import csv

def initialize_dict(types):
	temp_dict = {}
	for type1 in types:
		temp_dict[type1] = 0
	return temp_dict

def initialize_csv(aggregate_variable_name, out_csv_name):
	header = [aggregate_variable_name] + resource_types
	out_csv = open(out_csv_name, 'wb')
	csv_writer = csv.DictWriter(out_csv, delimiter= ',', fieldnames= header)
	csv_writer.writeheader()
	return (out_csv, csv_writer)

def initialize_variable_dict(aggregate_variables, resource_types):
	counts = initialize_dict(aggregate_variables)
	resources_dict = {}
	for aggregate_variable in aggregate_variables:
		resources_dict[aggregate_variable] = initialize_dict(resource_types)
	return counts, resources_dict


def aggregate_durations(row, aggregate_variable_name, counts, agg_resources_dict, resource_types):
	try:
		aggregate_variable = row[aggregate_variable_name]
		resources_dict = agg_resources_dict[aggregate_variable] #pick the resources_dict by the grade/country of the user
		for resource_type in resource_types:
				value = float(row[resource_type])
				resources_dict[resource_type] += value #add the value of each resource type to the total
		counts[aggregate_variable] += 1
	except KeyError:
		pass #grade or country is not in resources we are trying to capture

def write_agg_durations(aggregate_variable_name, aggregate_variables, counts, agg_resources_dict, resource_types, csv_writer):
	for aggregate_variable in aggregate_variables:
		resources_dict = agg_resources_dict[aggregate_variable] #pick the resources_dict by the grade/country of the user
		count = counts[aggregate_variable]
		for resource_type in resource_types:
			if count != 0:
				resources_dict[resource_type] /= count
		resources_dict[aggregate_variable_name] = aggregate_variable
		csv_writer.writerow(resources_dict)

if __name__ == "__main__":
	in_csv = open('duration_by_user_grade.csv')
	csv_reader = csv.DictReader(in_csv)
	grades = ['A', 'B', 'C']
	countries = ['US', 'IN', 'CH']

	fields = csv_reader.fieldnames
	assert('grade' == fields[0])
	assert('country' == fields[1])
	resource_types = fields[2:] #get the resource type names from the input csv

	out_csv_grade, grade_csv_writer = initialize_csv('grade', 'duration_aggregate_by_grade.csv')
	out_csv_country, country_csv_writer = initialize_csv('country', 'duration_aggregate_by_country.csv')

	grade_counts, grade_resources = initialize_variable_dict(grades, resource_types)
	country_counts, country_resources = initialize_variable_dict(countries, resource_types)

	#sum up the durations for each grade/country and resource_type
	for row in csv_reader:
		aggregate_durations(row, 'grade', grade_counts, grade_resources, resource_types)
		aggregate_durations(row, 'country', country_counts, country_resources, resource_types)

	# write the duration for each grade/country
	write_agg_durations('grade', grades, grade_counts, grade_resources, resource_types, grade_csv_writer)
	write_agg_durations('country', countries, country_counts, country_resources, resource_types, country_csv_writer)

	out_csv_grade.close()
	out_csv_country.close()
	in_csv.close()
