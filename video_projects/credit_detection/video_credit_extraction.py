#-​*- coding: UTF-8 -*​-
# coding=gbk

import json
import cv2
import numpy as np
import matplotlib.pyplot as plt 
import os
import csv
import time
import pysrt
from collections import deque

# both diff is in seconds
video_sub_end_diff = 350
video_backward_diff = 400
# skipping number in frames
skipping_number = 20


class FrameHistCalculater(object):

	# end of subtitle in seconds
	def getSubEndTime(self, subtitle_path):
		subtitle = pysrt.open(subtitle_path)
		end_of_sub = subtitle[-1].end
		end_time = self.transformToSeconds(end_of_sub.hours, end_of_sub.minutes, end_of_sub.seconds, end_of_sub.milliseconds)
		return end_time

	def transformToSeconds(swelf, hour, minute, seconds, milliseconds):
		result = ((((hour * 60) + minute) * 60) + seconds) + (float(milliseconds) / 1000)
		return result

	# return a bool to when provided with a frame
	def frameHistpolarization(self, frame):
		hist_numpy, bins = np.histogram(frame.ravel(),256,[0,256])

		# black and white approach but fail on some other colors
		# black_pixel_count = sum(hist_numpy[0: 3])
		# white_pixel_count = sum(hist_numpy[-3: ])

		# try to find the most dominating color in hist and calculate its precentange
		sorted_hist = np.sort(hist_numpy)
		polarized_pixel = sum(sorted_hist[-5 :])
		total_pixel_count = sum(hist_numpy)
		return float(polarized_pixel) / total_pixel_count

	def isCredit(self, blackNwhite_ratio, credit_buffer):
		credit_buffer.append(blackNwhite_ratio)
		credit_buffer.popleft()
		# print credit_buffer
		return credit_buffer

def main():
	# list of boxer movies and their path
	list_of_movie_path = open('video_files_for_computing.txt', 'r')
	movies = json.load(list_of_movie_path)
	movie_counter = 0
	FHC = FrameHistCalculater()
	for movie_id in movies:
		file_id = movie_id
		VIDEOPATH = movies[file_id]
		print file_id, VIDEOPATH
		subtitle_path = None
		credit_log_path = 'credit_log/with_ratio_' + str(file_id) + '.txt'
		print credit_log_path
		if os.path.isfile('credit_log/with_ratio_' + str(file_id) + '.txt'):
			movie_counter += 1
			print "finished number :{}".format(movie_counter)
			continue
		creditlog = open(credit_log_path, "w")
		movie_counter += 1
		print "finished number :{}".format(movie_counter)
		credit_buffer = deque([0] *5)


		#read video and get video parameters
		cap = cv2.VideoCapture(VIDEOPATH.encode("utf8"))
		length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
		width  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
		height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
		fps    = cap.get(cv2.cv.CV_CAP_PROP_FPS)
		print fps, length
		#read subtitles if there is any
		if subtitle_path == None:
			end_of_sub_time = length / fps
		else:
			subtitle = pysrt.open(subtitle_path)
			end_of_sub_time = FHC.getSubEndTime(subtitle_path)

		# get a start frame number to process
		if ((length / fps) - end_of_sub_time) > video_sub_end_diff:
			frame_number_start = int(end_of_sub_time * fps)

		else:
			frame_number_start = int(length - (video_backward_diff *fps))

		print "frame number to start {}".format(frame_number_start)
		frame_index = frame_number_start
		print frame_index

		# main loop to process
		while(cap.isOpened() and frame_index < length):
			cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_index)
			ret, frame = cap.read()
			if frame == None:
				break
			# print type(frame)
			ratio = FHC.frameHistpolarization(frame)
			# print ratio
			creditlog.write(str(frame_index) + '\n')
			creditlog.write(str(ratio) + '\n')
			frame_index += skipping_number


if __name__ == "__main__":
	main()