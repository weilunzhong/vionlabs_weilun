import json
from vionrabbit import *

rabbit = RabbitProducer('weilun_dynamic_multiple_credit')

movie_path = open("video_files_for_computing.txt")
movies = json.load(movie_path)

#use set operation to get the difference of lists since order in a list is not important
all_movie_set = set(movies.keys())

counter = 0
good_id_dict = {}
none_id_list = []
with open('credit_result/credit_time_with_length.json', 'r') as credit_stamp:
	for line in credit_stamp:
		movie_json = json.loads(line)
		if movie_json["credit_status"] == "single":
			counter += 1
			good_id_dict[movie_json["imdbID"]] = movie_json["start_credit"]
		elif movie_json["credit_status"] == "none":
			none_id_list.append(movie_json["imdbID"])
print len(good_id_dict.keys())
with open('credit_result/credit_time_multiple_0.7.json', 'r') as credit_stamp:
	for line in credit_stamp:
		movie_json = json.loads(line)
		if movie_json["credit_status"] == "single":
			counter += 1
			good_id_dict[movie_json["imdbID"]] = movie_json["start_credit"]
		elif movie_json["credit_status"] == "none":
			none_id_list.append(movie_json["imdbID"])
print len(good_id_dict.keys())
with open('credit_result/credit_time_multiple_0.75.json', 'r') as credit_stamp:
	for line in credit_stamp:
		movie_json = json.loads(line)
		if movie_json["credit_status"] == "single":
			counter += 1
			good_id_dict[movie_json["imdbID"]] = movie_json["start_credit"]
		elif movie_json["credit_status"] == "none":
			none_id_list.append(movie_json["imdbID"])

print len(none_id_list)
print len(good_id_dict.keys())

list_to_publish = list(set(none_id_list))
good_set = set(good_id_dict.keys())
none_set = set(none_id_list)

multiple_set = all_movie_set.difference(good_set)
multiple_set = multiple_set.difference(none_set)

multiple_id_list = list(multiple_set)
print len(multiple_id_list)

dynamic_dict = {}
with open("credit_result/dynamic_credit_with_time.json") as dynamic_stapm:
	for line in dynamic_stapm:
		movie_json = json.loads(line)
		if movie_json["imdbID"] in multiple_id_list:
			dynamic_dict[movie_json["imdbID"]] = movie_json["start_credit"]




print len(dynamic_dict.keys())

for ID in dynamic_dict.keys():
	message = {}
	message["imdbID"] = ID
	message["path"] = movies[ID]
	message["start_credit"] = dynamic_dict[ID]
	# print message
	rabbit.publish_dict(message)
	