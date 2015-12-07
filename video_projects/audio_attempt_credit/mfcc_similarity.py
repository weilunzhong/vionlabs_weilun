import json
import numpy as np
from scipy.spatial import distance
import os

mfcc_log_folder = "mfcc_log/12_monkey_2048/"

# def similarityMfcc(array_1, array_2):


# this function calculate the similarity between two mfcc series with the same window size
def windowSimiliraty(base_list, income_list, window_size):
	result_list =[]
	for i in range(0, window_size):
		income_mfcc_poped = income_list[i][1:]
		comparing_mfcc_poped = base_list[i][1:]
		income_array = np.asarray(income_mfcc_poped)
		comparing_array = np.asarray(comparing_mfcc_poped)
		result = distance.euclidean(income_array, comparing_array)
		result_list.append(result)
	return result_list

files = []
for (dirpath, dirnames, filenames) in os.walk(mfcc_log_folder):
	for element in filenames:
		files.append(os.path.splitext(element)[0])
	break
print files

base_name = files[0]
print base_name
with open(mfcc_log_folder + base_name +".json") as f1:
	data_1 = json.load(f1)
print len(data_1["lowlevel"]["mfcc"])

files.pop(0)

window_size = 20
start_frame = 5590

for index, name in enumerate(files):
	with open(mfcc_log_folder + name +".json") as f2:
		data_2 = json.load(f2)

	# indexing in seconds and from big bang s1e1
	# base_index = [160, 161, 162, 163]

	mfcc_list = data_1["lowlevel"]["mfcc"][start_frame:start_frame+window_size]

	final_result_list = []
	for index, income_mfcc in enumerate(data_2["lowlevel"]["mfcc"]):
		if index > 5900:
			break
		income_mfcc_list = data_2["lowlevel"]["mfcc"][index : index + window_size]
		result_list = windowSimiliraty(mfcc_list, income_mfcc_list, window_size)
		final_result_list.append(sum(result_list))

	ind = np.argmin(final_result_list)
	print final_result_list[ind - 20:ind + 20]
	print base_name, name
	print ind, min(final_result_list)
	print reduce(lambda x, y: x + y, final_result_list) / len(final_result_list)
	break