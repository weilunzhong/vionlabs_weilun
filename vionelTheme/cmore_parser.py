import openpyxl as px
import numpy as np
import re

boxer_ids = []
with open('imdbids_boxer.txt', 'r') as boxer_file:
	for line in boxer_file:
		boxer_ids.append(line[:9])
print len(boxer_ids)

def getWords(text):
	return re.compile('\w+').findall(text)

id_file = open('cmore_movie_ids.txt','w')

W = px.load_workbook('Movies.xlsx', use_iterators = True)
p = W.get_sheet_by_name(name = 'Sheet1')

a=[]

for row in p.iter_rows():
	for index,k in enumerate(row):
		if index:
			if k.internal_value:
				imdbID = getWords(k.internal_value)[-1]
				a.append(imdbID)
				if imdbID not in boxer_ids:
					id_file.write(imdbID + '\n')
print a

	