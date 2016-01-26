from frame_hist_calculator import FrameHistCalculator
#from vionmodels.research import EndCredit

def runtime():
	#path for all of them
	video_path = "/mnt/movies03/boxer_movies/tt1523483/[www.tnttorrent.info] Kaboom 2010 [DVDRip.XviD-miguel] [Ekipa TnT]/Kaboom 2010 [DVDRip.XviD-miguel] [ENG].avi"
	subtitle_path = None

	FHC = FrameHistCalculator()
	FHC.video_reader(video_path)
	start_frame = FHC.get_start_frame(subtitle_path)
	hist_res = FHC.frame_hist_calculation(start_frame)
	timestamp = FHC.set_timestamp(start_frame)
	print timestamp
	print hist_res
	#return EndCredit(data=hist_res, timestamps=timestamp)

if __name__ == "__main__":
	runtime()