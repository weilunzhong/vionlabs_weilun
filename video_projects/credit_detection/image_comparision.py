import cv2
import cv
import numpy as np
import os
import csv
import time
import json
import math

class image_similarioty_calculator(object):

	def __init__(self):
		pass

	def hogFeature(self, img):
		hog = cv2.HOGDescriptor()
		hog_result = hog.compute(img)
		return hog_result

	def similarityScoreHog(self, img1, img2):
		print img1.size
		hog_result_1 = self.hogFeature(img1)
		hog_result_2 = self.hogFeature(img2)
		print len(hog_result_1)
		error = 0
		for index, value in enumerate(hog_result_1):
			sub = value[0] - hog_result_2[index][0]
			error += math.pow(sub, 2)
		sqrt_error = math.sqrt(error)
		print sqrt_error
		self.hog_distance = sqrt_error

	def cpfFeature(self,img):
		cpf_result = cv2.resize(img, (20,20))
		return cpf_result

	def similarityScoreCpf(self, img1,img2):
		cpf_result_1 = self.cpfFeature(img1)
		cpf_result_2 = self.cpfFeature(img2)
		error = 0
		error_list = []
		for i in range(0,20):
			for j in range(0,20):
				sum_of_three = 0
				for k in range(0,3):
					error += abs(cpf_result_1[i][j][k] - cpf_result_2[i][j][k])
					sum_of_three += abs(cpf_result_1[i][j][k] - cpf_result_2[i][j][k])
					if sum_of_three> 700:
						print i,j,k
				error_list.append(sum_of_three)
		print error_list
		sqrt_error = error / 1200
		self.cpf_distance = sqrt_error 

	def histFeature(self, img):
		resized_img =cv2.resize(img,(100,100))
		hist_numpy, bins = np.histogram(resized_img.ravel(),256,[0,256])
		return hist_numpy

	def similarityScoreHist(self, hist_1, hist_2):
		error = 0
		error_list = []
		for index, value in enumerate(hist_1):
			error += abs(hist_1[index] - hist_2[index])
			error_list.append(abs(hist_1[index] - hist_2[index]))

		# print error_list
		self.hist_distance = float(error) / len(hist_1)


	def listHistRead(self, path_list):
		self.hist_list = []
		for path in path_list:
			# print path
			image = cv2.imread(path)
			hist = self.histFeature(image)
			self.hist_list.append(hist)


	def videoSearch(self, video_path, start_index, end_index, path_list, index_list):
		self.listHistRead(path_list)
		cap = cv2.VideoCapture(video_path)
		frame_index = start_index
		log_list1 = []
		log_list2 = []
		while(cap.isOpened()):
			cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_index)
			# print frame_index
			ret, frame = cap.read()
			if frame_index == None:
				break

			if frame_index > end_index:
				frame_index += 1
				break

			current_hist = self.histFeature(frame)
			lowerest_error = 30
			lowerest_error_index = 0
			for index, hist_single in enumerate(self.hist_list):
				self.similarityScoreHist(hist_single, current_hist)
				if lowerest_error > self.hist_distance:
					lowerest_error = self.hist_distance
					lowerest_error_index = index
			if lowerest_error < 25:
				log_list1.append(frame_index)
				log_list2.append(index_list[lowerest_error_index])
			frame_index += 1
		return log_list1, log_list2






# list of frames to be cached and compared with video sequence
list_index = [502, 1782, 1789, 1907, 1908, 1909, 1910, 1911, 1924, 1929, 1930, 2004, 2049, 2050, 2051, 2052, 2054, 2055, 2056, 2058, 2101, 2110, 2117, 2124, 2130, 2134, 2135, 2149, 2161, 2166, 2168, 2176, 2183, 2187, 2198, 2200, 2203, 2206, 2213, 2221, 2227, 2228, 2242, 2247, 2250, 2265, 2274, 2279, 2281, 2282, 2286, 2318, 2319, 2320, 2334, 2335, 2357, 2358, 2359, 2360, 2361, 2366, 2549, 2581, 4572, 4723, 4798]
#list_index = [2997]
path_list = map(lambda x: os.path.join("..", "movie_open_credit_data", "big_bang", "images", "full", ("big_bang_1-" + str(x)+ ".png")), list_index)

video_path = '../../weilun_thesis/die_another_day/big_bang_2.mp4'

cal = image_similarioty_calculator()
log1, log2 = cal.videoSearch(video_path, 1000, 2000, path_list, list_index)

for index, value in enumerate(log1):
	print abs(value - log2[index])



# error = cal.similarityScoreHist(img1, img2)
# print error


