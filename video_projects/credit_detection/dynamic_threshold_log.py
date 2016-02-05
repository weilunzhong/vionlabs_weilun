import json
import numpy as np
import re
from scipy import interpolate
import matplotlib.pyplot as plt 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DynamicLogHandler(object):

    def __init__(self):
        pass

    def _getWords(self, text):
        return re.compile('\w+').findall(text)

    def get_list_movies(self, video_file_path):
        # list of boxer movies and their path
        list_of_movie_file = open(video_file_path, 'r')
	movies = json.load(list_of_movie_file)
	return movies

    def _log_reader(self, movieid):
	log_folder = "credit_log/with_ratio_"
	log_file_path = log_folder + movieid + ".txt"
	log_file = open(log_file_path, "r")
	hist_result_array = np.zeros(1)
	time_stamp = np.zeros(1)
	for index, line in enumerate(log_file):
	    if (index % 2) == 0:
                time_stamp = np.append(time_stamp, int(self._getWords(line)[0]))
	    if (index % 2) ==1:
                hist_ratio = float(line[0:9])
                hist_result_array = np.append(hist_result_array, hist_ratio)
	hist_result_array = np.delete(hist_result_array, 0)
	time_stamp = np.delete(time_stamp, 0)
	# self.start_frame_index = time_stamp[0]
	# self.end_frame_index = time_stamp[-1]
	return hist_result_array, time_stamp

    def hist_smoothing(self, hist_result, kernel_size=2):
	smooth_hist_result = np.empty(hist_result.size)
	appending_array = np.zeros(kernel_size)
	hist_result = np.append(hist_result, appending_array)
	for index in range(0,smooth_hist_result.size):
            smooth_hist_result[index] = np.sum(hist_result[index: index + kernel_size]) / kernel_size
	return smooth_hist_result

    def interpolation(self, smoothed_hist, time_stamp, threshold):
	max_ratio = np.amax(smoothed_hist)
	min_ratio = np.amin(smoothed_hist)
	interpolation_value = min_ratio + threshold * (max_ratio - min_ratio)
	print max_ratio, min_ratio, interpolation_value
	estimation_func = np.poly1d(np.polyfit(time_stamp, smoothed_hist, 7))
	# flag_array = np.zeros(smoothed_hist.size)
	self.estimation_func = estimation_func
	index_array = np.where(estimation_func(time_stamp) > interpolation_value)
	return index_array

    def consecutive_index(self, index_array):
	consecutive_flag = False
	list_of_lists = []
        for index in index_array[0]:
	    if not consecutive_flag:
		current_list = [index]
		consecutive_flag = True
		pre_index = index
		continue
	    if consecutive_flag:
		if (index - pre_index) < 2:
                    current_list.append(index)
                    pre_index = index
		else:
		    list_of_lists.append(current_list)
		    current_list = [index]
		    pre_index = index
	list_of_lists.append(current_list)

	_, index_list = max(enumerate(list_of_lists), key = lambda tup: len(tup[1]))

	return index_list




    def single_log_handler(self, movieid):
	hist_result, time_stamp = self._log_reader(movieid)
	self.time_stamp = time_stamp
	if time_stamp.size == 0:
            return 0, 0
	else:
	    smoothed_hist = self.hist_smoothing(hist_result, 3)
	    self.smoothed_hist = smoothed_hist
	    index_array = self.interpolation(smoothed_hist, time_stamp, 0.7)
	    if index_array[0].size == 0:
                return 1, 1
	    else:
		index_list = self.consecutive_index(index_array)
		#print index_list
		start_credit = time_stamp[index_list[0]]
		end_credit = time_stamp[index_list[-1]]
		return int(start_credit), int(end_credit)
		# plt.show()


def main():
    log_folder = "credit_log/with_ratio_"
    DLH = DynamicLogHandler()
    credit_time_path = "dynamic_credit_with_time.json"
    credit_time_file = open(credit_time_path, 'w')
    movies = DLH.get_list_movies("video_files_for_computing.txt")
    for movieid in movies.keys():
	print "--"*10
	print movieid
	start_credit, end_credit = DLH.single_log_handler(movieid)
	credit_time_json = {}
	credit_time_json["imdbID"] = movieid
	credit_time_json["start_credit"] = start_credit
	credit_time_json["end_credit"] = end_credit
	credit_time_json["credit_duration"] = end_credit - start_credit
	credit_time_json["video_path"] = movies[movieid]
	json.dump(credit_time_json, credit_time_file)
	credit_time_file.write('\n')
    credit_time_file.close()

def test():
    log_folder = "credit_log/with_ratio_"
    DLH = DynamicLogHandler()
    """
    log_dynamic = open("credit_result/dynamic_credit_with_time.json", "r")
    for line in log_dynamic:
	credit_info = json.loads(line)
	if credit_info["start_credit"] == 1:
            continue
	else:
	    print bcolors.WARNING + str(credit_info["video_path"]) + bcolors.ENDC
	    print bcolors.FAIL + str(credit_info["start_credit"]) + bcolors.ENDC
	    #print credit_info["video_path"], credit_info["start_credit"]
	    start_credit, end_credit = DLH.single_log_handler(credit_info["imdbID"])
	    plt.plot(DLH.time_stamp, DLH.estimation_func(DLH.time_stamp), '.',DLH.time_stamp, DLH.smoothed_hist, '-')
	    plt.draw()
	    plt.pause(4)
	    # raw_input("<Hit Enter To Close>")
	    plt.close()
    """
    start_credit, end_credit = DLH.single_log_handler("tt1523483")
    plt.plot(DLH.time_stamp, DLH.estimation_func(DLH.time_stamp), '.',DLH.time_stamp, DLH.smoothed_hist, '-')
    plt.show()
	
if __name__ == "__main__":
    #main()
    test()
