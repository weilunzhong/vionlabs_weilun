from vionrabbit import VionWorker
import json

class WeilunEmptyQueueWorker(VionWorker):

    def process_json_dict(self, json_dict):
        print json_dict
        json.dump(json_dict, f)
        f.write("\n")


if __name__ == "__main__":
    f = open("credit_to_validate.json", 'wb')
    WeilunEmptyQueueWorker("weilun_credit_validation").work_it()
