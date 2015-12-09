import cv2
import numpy as np
import matplotlib.pyplot as plt 
import os
import csv
import time
import pysrt
from collections import deque


"""
# two credits with both scene background and fixed color background
input_video_path ='/mnt/databucket/movie_research/videofiles2/tt0303933/Drumline (2002)/Drumline.2002.720p.BrRip.x264.YIFY.mp4'
subtitle_path = '/mnt/databucket/movie_research/videofiles2/tt0303933/Drumline (2002)/Drumline.2002.720p.BrRip.x264.YIFY.srt'
"""

input_video_path = "/mnt/movies03/boxer_movies/tt0274166/Johnny English  (2003) 1080p x264 DD5.1 EN NL Subs [Asian torrenz]/Johhny English 2003 1080p.mkv"
subtitle_path = None


"""

# this path is a file with yellow credit background 
input_video_path = '/mnt/databucket/boxer_movies/tt1379182/Kynodontas.2009.PROPER.DVDRip.XviD.HORiZON-ArtSubs/Kynodontas.2009.PROPER.DVDRip.XviD.HORiZON-ArtSubs.avi'
subtitle_path = '/mnt/databucket/boxer_movies/tt1379182/Kynodontas.2009.PROPER.DVDRip.XviD.HORiZON-ArtSubs/Kynodontas.2009.PROPER.DVDRip.XviD.HORiZON-ArtSubs.srt'
"""




"""

# this path has credits displayed on pictures instead of fixed background
input_video_path = '/mnt/databucket/boxer_movies/tt0122151/Lethal Weapon 4 (1998) [1080p]/Lethal.Weapon.4.1998.1080p.BrRip.x264.BOKUTOX.YIFY.mp4'
subtitle_path = '/mnt/databucket/boxer_movies/tt0122151/Lethal Weapon 4 (1998) [1080p]/Lethal.Weapon.4.1998.1080p.BrRip.x264.BOKUTOX.YIFY.srt'
"""

# both diff is in seconds
video_sub_end_diff = 350
video_backward_diff = 400
# skipping number in frames
skipping_number = 20
credit_buffer = deque([0] *5)

# end of subtitle in seconds
def get_sub_end_time(subtitle_path):
	subtitle = pysrt.open(subtitle_path)
	end_of_sub = subtitle[-1].end
	end_time = transform_to_seconds(end_of_sub.hours, end_of_sub.minutes, end_of_sub.seconds, end_of_sub.milliseconds)
	return end_time

def transform_to_seconds(hour, minute, seconds, milliseconds):
	result = ((((hour * 60) + minute) * 60) + seconds) + (float(milliseconds) / 1000)
	return result

# return a bool to when provided with a frame
def frame_hist_polarization(frame):
	hist_numpy, bins = np.histogram(frame.ravel(),256,[0,256])

	# black and white approach but fail on some other colors
	# black_pixel_count = sum(hist_numpy[0: 3])
	# white_pixel_count = sum(hist_numpy[-3: ])

	# try to find the most dominating color in hist and calculate its precentange
	sorted_hist = np.sort(hist_numpy)
	polarized_pixel = sum(sorted_hist[-5 :])
	total_pixel_count = sum(hist_numpy)
	return float(polarized_pixel) / total_pixel_count

def is_credit(blackNwhite_ratio, credit_buffer):
	credit_buffer.append(blackNwhite_ratio)
	credit_buffer.popleft()
	print credit_buffer
	return credit_buffer

#read video and get video parameters
cap = cv2.VideoCapture(input_video_path)
length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
width  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.cv.CV_CAP_PROP_FPS)

print length
#read subtitles
if subtitle_path == None:
	end_of_sub_time = length / fps
else:
	subtitle = pysrt.open(subtitle_path)
	end_of_sub_time = get_sub_end_time(subtitle_path)

# get a start frame number to process
if ((length / fps) - end_of_sub_time) > video_sub_end_diff:
	frame_number_start = int(end_of_sub_time * fps)

else:
	frame_number_start = int(length - (video_backward_diff *fps))

print "frame number to start {}".format(frame_number_start)
frame_index = frame_number_start
# frame_index = 31678



# main loop to process
while(cap.isOpened()):
	cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_index)
	ret, frame = cap.read()
	# print type(frame)
	if frame == None:
		break
	ratio = frame_hist_polarization(frame)
	credit_buffer = is_credit(ratio, credit_buffer)
	buffer_avg = sum(credit_buffer) / 5
	if buffer_avg >0.65:
		frame_index += skipping_number
		cv2.putText(frame, "Yes", (15,50), cv2.FONT_HERSHEY_SIMPLEX, 1, cv2.cv.CV_RGB(0,255,0))
		cv2.imshow('frame', frame)
		print "Yes right now, frame index: {}".format(frame_index)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	else:
		frame_index += skipping_number
		cv2.putText(frame, "Not yet", (15,50), cv2.cv.CV_FONT_HERSHEY_SCRIPT_SIMPLEX, 1, cv2.cv.CV_RGB(255,0,0))
		cv2.imshow('frame', frame)
		print "Not yet, frame index: {}".format(frame_index)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# some code for alternative ways of plotting hist and RGB hist
	# maybe change to HSV encoding later to enhance performance
	"""
	cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_index)
	ret, frame = cap.read()
	hist = cv2.calcHist([frame],[0],None,[256],[0,256])
	hist_numpy, bins = np.histogram(frame.ravel(),256,[0,256])
	# print hist
	# print hist_numpy
	# print sum(hist_numpy[0: 3]), sum(hist_numpy[-3: ]), sum(hist_numpy)
	# plt.hist(frame.ravel(),256,[0,256]); plt.show()

	color = ('b','g','r')
	for i,col in enumerate(color):
		histr = cv2.calcHist([frame],[i],None,[256],[0,256])
		plt.plot(histr,color = col)
		plt.xlim([0,256])
	# plt.show()

	cv2.imshow('frame', frame)
	# frame_index += skipping_number
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	"""


print fps
cap.release()
cv2.destroyAllWindows()