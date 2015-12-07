from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
from pymongo import MongoClient


class GetListMovieId(object):

	def _get_words(self, text):
		return re.compile('\w+').findall(text)

	def _get_page_list(self, start_number):
		web_source = requests.get(self.page_url + str(start_number)).text
		soup = BeautifulSoup(web_source, "html.parser")
		page_movie_id_list = []
		for node in soup.findAll('div', class_='list_item'):
			list_node = node.find('div', class_='info')
			if list_node:
				node_link = list_node.b.a
				if self._get_words(node_link['href'])[0] == "title":
					page_movie_id_list.append(self._get_words(node_link['href'])[1])
		return page_movie_id_list

	def get_imdb_id(self, usr_list_id):
		self.page_url = "http://www.imdb.com/list/" + usr_list_id +"?start="
		web_source = requests.get(self.page_url + "1").text
		soup = BeautifulSoup(web_source, "html.parser")

		self.usr_list = {}
		self.usr_list["imdbID"] = usr_list_id


		list_title = soup.find('h1', {"class": "header"})
		description = soup.find('div', {"class": "description"})
		usr = soup.find('div', {"class": "byline"})
		if description:
			self.usr_list["description"] = description.text

		list_movie_id = []

		if list_title:
			self.usr_list["title"] = list_title.text
			
			self.usr_list["usr_id"] = self._get_words(usr.a["href"])[1]
			for i in range(0,20):
				start_number = 100*i +1
				list_movie_id.extend(self._get_page_list(start_number))
				print self._get_page_list(start_number)
				if len(self._get_page_list(start_number)) < 100:
					break

		self.usr_list["movie_list_id"] = list_movie_id

		return self.usr_list

class GetUsrListID(object):

	def __init__(self, movie_id):
		self.movie_id = movie_id

	def _get_words(self, text):
		return re.compile('\w+').findall(text)

	def get_usr_list_id(self):

		web_source = requests.get("http://www.imdb.com/lists/" + self.movie_id + "?ref_=tt_rls_sm").text
		soup = BeautifulSoup(web_source, "html.parser")


		self.usr_lists_id = []
		for node in soup.findAll('div', class_='list-preview'):
			# print node
			list_node = node.find('div', class_='list_name')
			#print list_node
			if list_node:
				node_link = list_node.b.a
				self.usr_lists_id.append(self._get_words(node_link['href'])[1])


class UsrIdToListId(object):

	def _get_words(self, text):
		return re.compile('\w+').findall(text)

	def get_usr_list_id(self, usr_id):

		web_source = requests.get("http://www.imdb.com/user/" + usr_id ).text
		soup = BeautifulSoup(web_source, "html.parser")


		self.usr_lists_id = []
		for node in soup.findAll('div', class_='user-list'):
			# print node
			list_node = node.find('a', class_='list-name')
			# print list_node['href'], "node"
			self.usr_lists_id.append(self._get_words(list_node['href'])[1])



GLMI = GetListMovieId()
list_dict = GLMI.get_imdb_id("ls003879468")
print list_dict, len(list_dict["movie_list_id"])

# GULI = GetUsrListID("tt1821549")
# GULI.get_usr_list_id()
# print GULI.usr_lists_id



"""
client = MongoClient('localhost', 27017)
db = client.imdb_usr_list
collection = db.list




with open('imdbids_boxer.txt', 'r') as imdbids_boxer_file:
	movie_list_imdbids = []
	for line in imdbids_boxer_file:
		movie_list_imdbids.append(re.compile('\w+').findall(line)[0])

movie_list_imdbids
for single_movie_id in movie_list_imdbids:
	print single_movie_id
	GULI = GetUsrListID(single_movie_id)
	try:
		GULI.get_usr_list_id()
	except:
		print "cant get the usrs"
	for single_usr_id in GULI.usr_lists_id:
		print single_usr_id
		check_data = collection.find_one({"imdbID": single_usr_id})
		if check_data:
			print "not inserting, already in there"
		else:
			GLMI = GetListMovieId(single_usr_id)
			try:
				usr_dict = GLMI.get_imdb_id()
				print usr_dict
				if len(usr_dict["movie_list_id"])>0:
					collection.insert(GLMI.usr_list)
			except:
				print "cant get movies"
		print collection.count()
		break
	break
"""