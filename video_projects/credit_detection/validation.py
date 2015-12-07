import json

credit_file = open('credit_time_multiple_0.8.json', 'r')
# credit_file = open('credit_time_with_length.json', 'r')
credit_dict = {}

for line in credit_file:
	line_json = json.loads(line)
	credit_dict[line_json['imdbID']] = line_json

# print credit_dict['tt0308644']

# values = credit_dict.itervalues()
# print values.next()
# print values.next()
most_certain = 0
too_short = 0
none = 0
multiple = 0
multiple_id_list = []
all_movies = credit_dict.keys()
for movieID in all_movies:
	if credit_dict[movieID]['credit_status'] == 'single' and credit_dict[movieID]['credit_length'] >= 1440:
		most_certain += 1
		# print most_certain
	elif credit_dict[movieID]['credit_status'] == 'single' and credit_dict[movieID]['credit_length'] < 1440:
		print credit_dict[movieID]['credit_length'], movieID
		too_short += 1

	if credit_dict[movieID]['credit_status'] == 'multiple':
		multiple += 1
		multiple_id_list.append(movieID)

	if credit_dict[movieID]['credit_status'] == 'none':
		none += 1
		#print movieID
print most_certain, 'most_certain'
print too_short, 'too short'
print multiple, 'multiple'
print none, 'none'
# print multiple_id_list