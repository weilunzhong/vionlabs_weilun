import json
import re

def getWords(text):
	return re.compile('\w+').findall(text)

imdb_id = open('imdbids_boxer.txt', 'r')
id_list = []
for line in imdb_id:
	id_list.append(getWords(line)[0])



match_index = 0
unmatch_index = 0
plot_extracted_path = 'output/city_extracted_3class_plots_fixed_with_imdbid.json'
plot_extracted_file = open(plot_extracted_path, 'r')
boxer_extracted_path = 'output/city_extracted_3class_plots_boxer_fixed.json'
boxer_extracted_file = open(boxer_extracted_path, 'w')
for each_movie_extracted in plot_extracted_file:
	name_entity = json.loads(each_movie_extracted)
	if 'IMDBID' in name_entity:
		if name_entity['IMDBID'] in id_list:
			match_index += 1
			json.dump(name_entity, boxer_extracted_file)
			boxer_extracted_file.write('\n')
		else:
			unmatch_index += 1

boxer_extracted_file.close()

print match_index, unmatch_index
