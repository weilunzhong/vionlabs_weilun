import json

with open('vionel_research/recommender_libs/actor_imdbids.json') as actor_imdb_list:
	actor_imdb_dict = json.loads(actor_imdb_list.readline())

output_data = open('famous_actor_imdbids.json', 'w')


# print actor_imdb_dict['nm0000093']
all_actor = actor_imdb_dict.keys()
print len(all_actor)
famous_actor = {}
famous_counter = 0
for actor in all_actor:
	if len(actor_imdb_dict[actor]) > 7:
		famous_counter += 1
		famous_actor[actor] = actor_imdb_dict[actor]


json.dump(famous_actor, output_data)
output_data.close()

print famous_counter