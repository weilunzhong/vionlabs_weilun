import json
import numpy as np
from scipy.spatial import distance
import os

"""
This class takes two mfcc log and calculate the shift between the two audios
Time is represented in 0.1s
"""

class PositionDetector(object):

	def __init__ (self, mfcc_log_folder, base_name, compare_name):
		self.window_size = 20
		self.sample_dist =20
		self.mfcc_log_folder = mfcc_log_folder
		self.base_name = base_name
		self.compare_name = compare_name

	# this function returns two lists of mfccs for further calculation
	def load_log(self):
		with open(self.mfcc_log_folder + self.base_name +".json") as f1:
			data_1 = json.load(f1)
		with open(self.mfcc_log_folder + self.compare_name +".json") as f2:
			data_2 = json.load(f2)
		self.base_mfcc_list = data_1["lowlevel"]["mfcc"]
		self.compare_mfcc_list = data_2["lowlevel"]["mfcc"]
		self.mfcc_length = len(data_1["lowlevel"]["mfcc"])


	# this function calculate the similarity between two mfcc series with the same window size
	# ie first layer search
	def _window_similiraty(self, base_list, income_list, window_size):
		result_list =[]
		for i in range(0, window_size):
			income_mfcc_poped = income_list[i][1:]
			comparing_mfcc_poped = base_list[i][1:]
			income_array = np.asarray(income_mfcc_poped)
			comparing_array = np.asarray(comparing_mfcc_poped)
			result = distance.euclidean(income_array, comparing_array)
			result_list.append(result)
		return sum(result_list)

	# this fuction calculate the sim between two fix length allined vectors
	# ie second layer search and return a list to process
	def _window_sim_single(self, base_list, income_list):
		result_list = []
		print len(base_list)
		for i in range(0, len(base_list)):
			base_mfcc_poped = base_list[i][1:]
			income_mfcc_poped = income_list[i][1:]
			income_array = np.asarray(income_mfcc_poped)
			base_array = np.asarray(base_mfcc_poped)
			result = distance.euclidean(income_array, base_array)
			result_list.append(int(result))
		return result_list


	# this function loop through all base segments and get the smallest sim measure and get the displacement
	def position_loop(self):
		self.loop_result_dict = {}
		smallest_dist = 10000
		for index in range(1,(self.mfcc_length/self.sample_dist)):
			print index
			print smallest_dist
			base_list = self.base_mfcc_list[index * self.sample_dist: index * self.sample_dist+self.sample_dist]
			single_position_result_list = []
			for income_index in range(0,self.mfcc_length-2*self.window_size):
				income_mfcc_list = self.compare_mfcc_list[income_index: income_index + self.window_size]
				cum_result = self._window_similiraty(base_list, income_mfcc_list, self.window_size)
				single_position_result_list.append(cum_result)
			if min(single_position_result_list) < smallest_dist and min(single_position_result_list)>10:
				smallest_dist = min(single_position_result_list)
				self.matched_base_index = index *20
				self.matched_income_index = np.argmin(single_position_result_list)
				self.diff = self.matched_base_index - self.matched_income_index

	# given the displacement of the two audio, calculate the second layer sim and pass it on in a list
	def length_extractor(self):
		# self.diff = -15
		if self.diff > 0:
			truncated_base_list = self.base_mfcc_list[self.diff:]
			truncated_compare_list = self.compare_mfcc_list[:len(truncated_base_list)]
			self.front_flag = True
		else:
			truncated_compare_list = self.compare_mfcc_list[abs(self.diff):]
			truncated_base_list = self.base_mfcc_list[:len(truncated_compare_list)]
			self.front_flag = False

		self.result_list = self._window_sim_single(truncated_base_list, truncated_compare_list)
		self.result_list

	def length_list_filter(self):

		if self.front_flag:
			index_to_print = [i+self.diff for i, value in enumerate(self.result_list) if value < 30]
		else:
			index_to_print = [i for i, value in enumerate(self.result_list) if value < 30]
		frame_last = 0
		# print index_to_print
		in_credit_flag = False
		self.credit_time_dict = {}
		list_counter = 0
		for element in index_to_print:
			frame_current = element
			# print frame_current, frame_last, in_credit_flag
			if frame_current-frame_last < 20:
				if in_credit_flag == False:
					list_counter += 1
					self.credit_time_dict[list_counter] = []
					self.credit_time_dict[list_counter].append(frame_current)
					in_credit_flag = True
				else:
					self.credit_time_dict[list_counter].append(frame_current)
			else:
				in_credit_flag = False



			frame_last = frame_current

		longset_index = max(self.credit_time_dict, key=lambda x:len(self.credit_time_dict[x]))
		self.credit_start = self.credit_time_dict[longset_index][0]
		self.credit_end = self.credit_time_dict[longset_index][-1]



if __name__ == '__main__':
	PD = PositionDetector('mfcc_log/house_2048/', 'house_of_cards_1_2048', 'house_of_cards_2_2048')
	PD.load_log()
	PD.position_loop()
	PD.length_extractor()
	# print PD.result_list, "result"
	# print PD.front_flag

	PD.length_list_filter()
	print PD.credit_start, PD.credit_end