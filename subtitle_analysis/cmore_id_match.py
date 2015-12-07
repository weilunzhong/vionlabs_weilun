import json

boxer_id_path = '../recommendation/boxer_movies.dat'
cmore_id_path = 'exported.jl'
counter = 0

vid_iid_dict = {}
with open(boxer_id_path, 'r') as boxer_movies:
	for line in boxer_movies:
		movie_data = json.loads(line)
		vid_iid_dict[movie_data["vionelID"]] = movie_data["imdbId"]

all_cmore_vid = vid_iid_dict.keys()
print len(all_cmore_vid)

with open(cmore_id_path, 'r') as cmore_movies:
	for line in cmore_movies:
		cmore_movie_data = json.loads(line)
		cmore_vid = cmore_movie_data["vionElement"]["vionelID"]
		if cmore_vid in all_cmore_vid:
			counter += 1


print counter