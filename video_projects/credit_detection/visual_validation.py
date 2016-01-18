import cv2
import json
from vionrabbit import *


class WeilunWorker(VionWorker):

	def process_json_dict(self, json_dict):
		video_path = json_dict['path']
		imdbID = json_dict['imdbID']
		start_credit = json_dict['start_credit']
		print "-" * 10
		# start_credit = 0
		result = self.play_credit(video_path, start_credit)
		print "this is the result: ", result
		print video_path
		if result:			rabbit_wrong.publish_dict(json_dict)
		#raise ValueError

	def play_credit(self, video_path, start_credit):
		cap = cv2.VideoCapture(video_path.encode("utf8"))
		length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
		#frame_index = start_credit[0] + 100
		frame_index = int(start_credit) - 100
		print "start from: ", start_credit, length
		while(cap.isOpened() and frame_index < length):
			cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_index)
			ret, frame = cap.read()
			frame_index += 10
			cv2.imshow('frame', frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord('w'):
				return False
				cap.release()
				cv2.destroyAllWindows()
				break
			elif key == ord('r'):
				return True
				cap.release()
				cv2.destroyAllWindows()
				break



def main():
	rabbit_right = RabbitProducer('weilun_credit_right')
	rabbit_wrong = RabbitProducer('weilun_credit_wrong')
	WeilunWorker("weilun_credit_validation").work_it()
	#WW.work_it()

if __name__ == "__main__":
	rabbit_right = RabbitProducer("weilun_dynamic_multiple_credit")
	rabbit_wrong = RabbitProducer("weilun_dynamic_multiple_credit")
	WeilunWorker("weilun_dynamic_multiple_credit").work_it()
