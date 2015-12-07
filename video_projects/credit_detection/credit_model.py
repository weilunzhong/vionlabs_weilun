from researchbase import TemporalVionFeature, 



class HistResultModel(TemporalVionFeature):

	"""
		this model store the dominating hist ratio at the end of a movie, this is to replace a log file
		sampling rate is 20/frame_rate
		start_time = (movie_length - wait_time * skip_frame) in microseconds
	"""
	pass

class MovieCreditModel():
	pass 

class EnvironmentFullClass(TemporalVionFeature):

	"""
		This model is for the prediction of each frame, aka replace the log file
		sampling rate is the inverse of skipping frame number
		start_time is the start of the movie
		205 classed are presented here
	"""

	labels = [AxisLabels(axis=1, labels=[list_loaded_from_csv])]


class EnvironmentMergedClass(TemporalVionFeature):

	"""
		only difference is this only contains 28 classes and added likely a face category
	"""
	labels = [AxisLabels(axis=1, labels=[list_loaded_from_csv)]