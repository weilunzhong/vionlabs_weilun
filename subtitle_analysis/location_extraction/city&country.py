import sys
import csv
import json
import pprint

'''
city_country_output = open('city_country.json', 'w')
list_of_cities = list(csv.reader(open('cities15000.txt', 'rb'), delimiter='\t'))
for element in list_of_cities:
	#print element[1], element[8]
	data = {'CITY_CODE': element[0], 'CITY': element[2], 'COUNTRY_CODE' : element[8]}
	json.dump(data,city_country_output)
	city_country_output.write('\n')

city_country_output.close()
'''

country_code_output = open('country_with_code.json', 'w')
country_code = open('country_code.json', 'r')
data = json.load(country_code)
for element in data:
	output_data = {'COUNTRY_NAME':element['Name'], 'COUNTRY': []}
	json.dump(output_data, country_code_output)
	country_code_output.write('\n')

country_code_output.close()
