import json
import numpy as np
import matplotlib.pyplot as plt 
import os
import csv
import time
import pysrt
import re

class LogHandler(object):

	def __init__(self, log_folder, sliding_window_size, filter_ratio, wait_time, skip_frame):
		self.log_folder = log_folder
		self.sliding_window_size = sliding_window_size
		self.filter_ratio =filter_ratio
		self.wait_time = wait_time
		self.skip_frame = skip_frame

	def _getWords(self, text):
		return re.compile('\w+').findall(text)

	def _arraySlidingWindow(self, result_array, sliding_window_size, filter_ratio):
		array_length = np.size(result_array)
		buffer_array = np.zeros((1), dtype = np.int)

		for index in range(0, array_length - sliding_window_size):
			window_score = np.sum(result_array[index: index + sliding_window_size])
			if window_score > (sliding_window_size * filter_ratio):
				buffer_array = np.append(buffer_array, 1)
			else:
				buffer_array = np.append(buffer_array, 0)

		buffer_array= np.delete(buffer_array, 0)
		print buffer_array
		length = np.size(buffer_array)
		flag_array = np.zeros((length), dtype = np.int)
		pre_value = 0
		for buffer_index , value in enumerate(buffer_array):
			if (pre_value - value) == -1:
				flag_array[buffer_index] = 1
			elif(pre_value - value) == 1:
				flag_array[buffer_index] = -1
			else:
				pass
			pre_value = value
		print flag_array
		return flag_array


	def get_list_movies(self, video_file_path):
		# list of boxer movies and their path
		list_of_movie_file = open(video_file_path, 'r')
		movies = json.load(list_of_movie_file)
		return movies

	def single_log_handler(self, movieid):
		credit_time_json = {}
		credit_time_json["imdbID"] = movieid
		hist_result_array = np.zeros(1)
		log_file_path = self.log_folder + movieid + ".txt"
		log_file = open(log_file_path, "r")
		for index, line in enumerate(log_file):
			if index == 0:
				start_frame_index = int(self._getWords(line)[0])
				end_frame_index = start_frame_index + self.wait_time * self.skip_frame
				#print start_frame_index
			if (index % 2) ==1:
				hist_ratio = float(line[0:9])
				hist_result_array = np.append(hist_result_array, hist_ratio)

		hist_result_array = np.delete(hist_result_array, 0)
		result = self._arraySlidingWindow(hist_result_array, self.sliding_window_size, self.filter_ratio)
		start_credit = np.argwhere(result == 1)
		end_credit = np.argwhere(result == -1)
		print start_credit, end_credit
		start_credit_list = []
		end_credit_list = []

		for time in start_credit:
			if time[0] < 460:
				start_credit_list.append(start_frame_index + (time[0] * 20))
		for time in end_credit:
				end_credit_list.append(start_frame_index + (time[0] * 20))

		if len(start_credit_list) == 1 and len(end_credit_list) <= 1:
			credit_time_json['credit_status'] = "single"
			credit_time_json['start_credit'] = start_credit_list
			credit_time_json['end_credit'] = end_credit_list
			if len(end_credit_list) == 1:
				credit_time_json['end_diff'] = end_frame_index - end_credit_list[0]
				end_frame_index = min(end_credit_list[0], end_frame_index)
			credit_time_json['credit_length'] = end_frame_index - start_credit_list[0]
		elif len(start_credit_list) > 1:
			credit_time_json['credit_status'] = "multiple"
			credit_time_json['start_credit'] = start_credit_list
			credit_time_json['end_credit'] = end_credit_list
		elif len(start_credit_list) == 0 and len(end_credit_list) == 0:
			credit_time_json['credit_status'] = "none"
			credit_time_json['start_credit'] = start_credit_list
			credit_time_json['end_credit'] = end_credit_list

		else:
			credit_time_json['start_credit'] = start_credit_list
			credit_time_json['end_credit'] = end_credit_list
			credit_time_json['credit_status'] = "weird"

		return credit_time_json



	def result_writer(self):
		credit_time_file = open(self.credit_time_path, 'w')
		movies = self.get_list_movies(self.video_file_path)
		for movieid in movies.keys():
			credit_time_json = self.single_log_handler(movieid)
			json.dump(credit_time_json, credit_time_file)
			credit_time_file.write('\n')
		credit_time_json.close()



def main():
	sliding_window_size = 20
	filter_ratio = 0.7
	wait_time = 480
	skip_frame = 20
	log_folder = "credit_log/with_ratio_"
	LH = LogHandler(log_folder, sliding_window_size, filter_ratio, wait_time, skip_frame)
	credit_time_path = "credit_with_time.json"
	credit_time_file = open(credit_time_path, 'w')
	movies = LH.get_list_movies("video_files_for_computing.txt")
	good_ones_counter = 0
	multiple_start_counter = 0
	multiple_start_list =[]
	no_start_counter = 0
	no_start_list =[]
	for movieid in movies.keys():
		credit_time_json = LH.single_log_handler(movieid)
		if credit_time_json["credit_status"] == "single":
			good_ones_counter += 1
		elif credit_time_json["credit_status"] == "multiple":
			multiple_start_counter += 1
			multiple_start_list.append(credit_time_json["imdbID"])
		elif credit_time_json["credit_status"] == "none":
			no_start_counter += 1
			no_start_list.append(credit_time_json["imdbID"])
		json.dump(credit_time_json, credit_time_file)
		credit_time_file.write('\n')
	credit_time_file.close()

	print good_ones_counter, "number that I am sure"
	print multiple_start_counter, "number that have multiple start"
	print no_start_counter, "number that got no credit"

	print multiple_start_list
	print no_start_list


def single_log():
	sliding_window_size = 20
	filter_ratio = 0.7
	wait_time = 500
	skip_frame = 20
	log_folder = "credit_log/with_ratio_"
	LH = LogHandler(log_folder, sliding_window_size, filter_ratio, wait_time, skip_frame)
	movieid = "tt0206917"
	credit_time_json = LH.single_log_handler(movieid)
	print credit_time_json

if __name__ == "__main__":
	single_log()
