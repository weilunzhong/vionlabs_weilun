from vionrabbit import VionWorker

"""
rabbit = RabbitProducer('queue name')
rabbit.publishdicts()

"""

class WeilunWorker(VionWorker):

	def process_json_dict(self, json_dict):
		
		print json_dict



if __name__ == "__main__":
	WeilunWorker("weilun_testing").work_it()
	#WW.work_it()