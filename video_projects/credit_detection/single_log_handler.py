import json
import numpy as np
import matplotlib.pyplot as plt 
import os
import csv
import time
import pysrt
import re


log_file_folder = 'credit_log/with_ratio_'
credit_time_path = 'credit_time_in_frames.json'


def getWords(text):
	return re.compile('\w+').findall(text)

def arraySlidingWindow(result_array, sliding_window_size, filter_ratio):
	array_length = np.size(result_array)
	buffer_array = np.zeros((1), dtype = np.int)

	for index in range(0, array_length - sliding_window_size):
		window_score = np.sum(result_array[index: index + sliding_window_size])
		if window_score > (sliding_window_size * filter_ratio):
			buffer_array = np.append(buffer_array, 1)
		else:
			buffer_array = np.append(buffer_array, 0)

	buffer_array= np.delete(buffer_array, 0)
	# print buffer_array
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
	return flag_array

movies = [u'tt0302640', u'tt2199571', u'tt0091187', u'tt0228750', u'tt1433207']



for movieid in movies:
	credit_time_json = {}
	credit_time_json['imdbID'] = movieid
	# use array to store the hist result
	hist_result_array = np.zeros(1),
	log_file_path = log_file_folder + movieid + '.txt'
	log_file = open(log_file_path, 'r')
	for index, line in enumerate(log_file):
		if index == 0:
			start_frame_index = int(getWords(line)[0])
			#print start_frame_index
		if (index % 2) ==1:
			hist_ratio = float(line[0:9])
			hist_result_array = np.append(hist_result_array, hist_ratio)

	hist_result_array = np.delete(hist_result_array, 0)
	# print hist_result_array
	result = arraySlidingWindow(hist_result_array, 20, 0.55)
        print "################"
	print result, len(result)

	start_credit = np.argwhere(result == 1)
	end_credit = np.argwhere(result == -1)
	print start_credit, end_credit
	start_credit_list = []
	end_credit_list = []
        print "################"
