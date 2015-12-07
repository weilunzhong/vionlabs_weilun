import json
import re
import pprint


location_file_path = '../stanford-ner-2015-04-20/Inputs_Outputs/outputs/'
table_path = 'fid_wid_iid.txt'


def get_wiki_id(imdb_id, table_path):
	id_table = open(table_path, 'r')
	for line in id_table:
		ids = getWords(line)
		if ids[3] == imdb_id:
			return ids

def getWords(text):
	return re.compile('\w+').findall(text)

bond_id_list = open ('bond_list.txt', 'r')
id_table = open(table_path, 'r')
for line in bond_id_list:
	ids = getWords(line)
	bond_id = ids[0]
	wiki_id = get_wiki_id(bond_id, table_path)
	#wiki_id[3]
	with open('../stanford-ner-2015-04-20/Inputs_Outputs/outputs/'+ wiki_id[2] +'.json') as data_file:
		data = json.load(data_file)
		print '----------'
		#print data['LOCATION']
		print line
		for element in data['LOCATION']:
			list_file = open('country_with_code.json')
			for country_entity in list_file:
				#print country_entity
				list_of_country = json.loads(country_entity)
				if element == list_of_country['COUNTRY_NAME']:
					print element



# country_list = open('country_list.txt', 'r')
# for country in country_list:
# 	print country
# 	if country == 'Jamaica':
# 		print country
