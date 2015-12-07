#!coding=utf-8
import json
import math
from collections import Counter
import os

def addLocationCountry(country_path, boxer_json_data):
	boxer_json_data['locationCountry'] = {}
	with open(country_path, 'r') as country_file:
		for movie_country_line in country_file:
			movie_country_json = json.loads(movie_country_line)
			if movie_country_json['IMDBID'] == boxer_json_data['imdbId']:
				for index, country_in_movie in enumerate(movie_country_json['COUNTRY_NAME']):
					boxer_json_data['locationCountry'][movie_country_json['COUNTRY_NAME'][index]] = movie_country_json['COUNTRY_CODE'][index]
			else:
				continue

	return boxer_json_data


def addLocationState(state_path, boxer_json_data):
	boxer_json_data['locationState'] = {}
	with open(state_path, 'r') as state_file:
		for movie_state_line in state_file:
			movie_state_json = json.loads(movie_state_line)
			if movie_state_json['IMDBID'] == boxer_json_data['imdbId']:
				for index, state_in_movie in enumerate(movie_state_json['STATE']):
					boxer_json_data['locationState'][movie_state_json['STATE'][index]] = movie_state_json['COUNTRY_CODE'][index]
			else:
				continue

	return boxer_json_data


def addLocationCity(city_path, boxer_json_data):
	boxer_json_data['locationCity'] = {}
	with open(city_path, 'r') as city_file:
		for movie_city_line in city_file:
			movie_city_json = json.loads(movie_city_line)
			if movie_city_json['IMDBID'] == boxer_json_data['imdbId']:
				for index, city_in_movie in enumerate(movie_city_json['CITY']):
					boxer_json_data['locationCity'][movie_city_json['CITY'][index]] = movie_city_json['COUNTRY_CODE'][index]
			else:
				continue

	return boxer_json_data


def addVionScene (scene_path, boxer_json_data):
	boxer_json_data['vionScene'] = {}
	with open(scene_path, 'r') as scene_file:
		for movie_scene_line in scene_file:
			movie_scene_json = json.loads(movie_scene_line)
			if movie_scene_json['imdb_id'] == boxer_json_data['imdbId']:
				for index, scene_in_movie in enumerate(movie_scene_json['scene_tag']):
					boxer_json_data['vionScene'][scene_in_movie.keys()[0]] = scene_in_movie.values()[0]

			else:
				continue

	return boxer_json_data





country_path = '/home/vionlabs/Documents/subtitle_analysis/location_extraction/output/country_extracted_3class_plots_imdb_boxer.json'
state_path = '/home/vionlabs/Documents/subtitle_analysis/location_extraction/output/states_extracted_3class_plots_imdb_boxer.json'
city_path = '/home/vionlabs/Documents/subtitle_analysis/location_extraction/output/city_extracted_3class_plots_boxer_fixed.json'
scene_path = '/home/vionlabs/Documents/recommendation/boxer_scene_output.json'
boxer_source_path = '/home/vionlabs/Documents/recommendation/boxer_movies.dat'
boxer_output_path = '/home/vionlabs/Documents/recommendation/boxer_movies_with_scene.json'
with open(boxer_source_path, 'r') as boxer_data:
	output_file = open(boxer_output_path, 'w')
	for line_index, line in enumerate(boxer_data):
		boxer_json_data = json.loads(line)
		boxer_json_data = addLocationCountry(country_path, boxer_json_data)
		boxer_json_data = addLocationState(state_path, boxer_json_data)
		boxer_json_data = addLocationCity(city_path, boxer_json_data)
		boxer_json_data = addVionScene(scene_path, boxer_json_data)
		json.dump(boxer_json_data, output_file)
		output_file.write('\n')
		print line_index

	output_file.close()