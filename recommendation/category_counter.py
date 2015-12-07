import json


class tag_handler:

	def tagAppend():
		

scene_tag = open('boxer_scene_output.json', 'r')
tag_object = {}
for line in scene_tag:
	movie_scene = json.loads(line)
	for element in movie_scene['scene_tag']:
		if element.keys()[0] not in tag_object:
			tag_object[element.keys()[0]] = 1
		else:
			tag_object[element.keys()[0]] += 1

print tag_object

