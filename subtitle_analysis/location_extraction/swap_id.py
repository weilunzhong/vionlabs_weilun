import json
import re

def getWords(text):
	return re.compile('\w+').findall(text)


def createIdDict(id_list_path):
	id_dict = {}
	id_list = open(id_list_path, 'r')
	for line in id_list:
		ID = getWords(line)
		id_dict[ID[2]] = ID[3]
	return id_dict

def swapWikiWithImdb(id_dict, input_file_location, output_file_location):
	after_the_swap = open(output_file_location, 'w')
	to_be_swapped = open(input_file_location, 'r')
	nomatch_counter = 0
	for each_movie_item in to_be_swapped:
		data_out = json.loads(each_movie_item)
		#print data_out['ID']
		if data_out['ID'][0] in id_dict:
			data_out['IMDBID'] = id_dict[data_out['ID'][0]]
			json.dump(data_out, after_the_swap)
		else:
			nomatch_counter += 1
			print 'no match', data_out['ID'], nomatch_counter
			json.dump(data_out, after_the_swap)
		after_the_swap.write('\n')
	after_the_swap.close()



id_list_path = '/home/vionlabs/Documents/subtitle_analysis/location_extraction/fid_wid_iid.txt'
input_path = '/home/vionlabs/Documents/subtitle_analysis/location_extraction/output/city_extracted_plots_boxer_fixed.json'
output_path = '/home/vionlabs/Documents/subtitle_analysis/location_extraction/output/city_extracted_plots_boxer_fixed_imdb.json'
id_dict = createIdDict(id_list_path)
swapWikiWithImdb(id_dict, input_path, output_path)