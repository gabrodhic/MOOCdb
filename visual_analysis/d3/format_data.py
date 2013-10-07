import csv

unformatted_data = csv.DictReader(open('duration_by_resource_type.csv'))
formatted_data = csv.writer(open('duration_by_resource_type_formatted.csv', 'wb'))

resource_list = ['State']
duration_list = ['All Students']
for row in unformatted_data:
	duration = row['total_duration']
	resource_type = row['resource_type_name+']
	if resource_type != 'unknown' and resource_type != 'testing' and resource_type != 'info':
		resource_list.append(resource_type)
		duration_list.append(duration)

formatted_data.writerow(resource_list)
formatted_data.writerow(duration_list)
