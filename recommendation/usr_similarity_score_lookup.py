import json

file_path = 'actor_coefficient.json'
json_file = open(file_path, 'r')

for line in json_file:
	tmp_data = json.loads(line)
	if tmp_data.keys()[0] == 'nm0413168':
		dict_data = tmp_data['nm0413168']
		sorted_x = sorted(dict_data.items(), key=operator.itemgetter(1))
		print sorted_x
