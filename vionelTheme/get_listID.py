from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re

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




UTL = UsrIdToListId()
UTL.get_usr_list_id("ur31140108")
print UTL.usr_lists_id