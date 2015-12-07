import json

boxer_ids = []
with open('imdbids_boxer.txt', 'r') as boxer_file:
	for line in boxer_file:
		boxer_ids.append(line[:9])
print len(boxer_ids)



telia_id_file = open('telia_id.txt', 'w')

telia_id_list = []
with open('reconciled_telia.jl', 'r') as telia_file:
	for line in telia_file:
		data = json.loads(line)
		# print data['externalIDs']['imdbID']
		if data['externalIDs']['imdbID'] not in boxer_ids:
			telia_id_list.append(data['externalIDs']['imdbID'])

print len(list(set(telia_id_list)))
telia_list = list(set(telia_id_list))
for element in telia_list:
	telia_id_file.write(element + '\n')