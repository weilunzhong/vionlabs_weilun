import os
import essentia as es
import matplotlib.pyplot as plt
import essentia.standard as estd
import essentia.streaming as estr
import pylab
from pylab import plot, show, figure


"""
This script takes a folder of viedo files and perform mfcc to each single one of them
stop_pool_num determine if process the whole video or cut off at certain time(in seconds)
default sample rate is 14000
frame size 2048, hopsize 1400(0.1s)
"""

audio_folder = "/media/weilun/tv_series/audio_file/wel/"

from os import walk

files = []
for (dirpath, dirnames, filenames) in walk(audio_folder):
	for element in filenames:
		files.append(os.path.splitext(element)[0])
	break
print files


stop_pool_num = 6000
format_name = ".wav"

for name in files:
	print name
	audio_path = audio_folder + name +format_name
	json_path = "mfcc_log/" + name + "_2048.json"


	loader = estd.MonoLoader(filename = audio_path, sampleRate=14000)
	audio = loader()

	w = estd.Windowing(type = 'hann')
	spectrum = estd.Spectrum()
	mfcc = estd.MFCC()
	loudness = estd.Loudness()




	pool = es.Pool()

	frame_counter = 0
	for frame in estd.FrameGenerator(audio, frameSize = 2048, hopSize = 1400):
		if frame_counter > stop_pool_num:
			break
		frame_counter += 1
		mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
		pool.add('lowlevel.mfcc', mfcc_coeffs)
		pool.add('lowlevel.mfcc_bands', mfcc_bands)

	print frame_counter

	estd.YamlOutput(filename = json_path, format = "json")(pool)

