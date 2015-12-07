class bcolors:
    HEADER = '\033[95m'#purple
    OKBLUE = '\033[94m'#blue
    OKGREEN = '\033[92m'#green
    WARNING = '\033[93m'#yello
    FAIL = '\033[91m'#red
    ENDC = '\033[0m'


def wiki_address_to_wiki_info(a):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	PREFIX dbpprop: <http://dbpedia.org/property/>
	PREFIX sn: <"""+a+""">
	SELECT   ?h ?wid ?type 
	WHERE {
	  ?h dbo:wikiPageID ?wid .
	  ?h foaf:isPrimaryTopicOf sn:.
	  
	} 
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results["results"]["bindings"]

def wiki_address_to_freebase_info(a):
	sparql = SPARQLWrapper("http://lod.openlinksw.com/sparql")
	sparql.setQuery("""
	PREFIX ns: <http://rdf.freebase.com/ns/>
	PREFIX sn: <"""+a+""">
	select  ?f ?typeid ?ew where {
	?f ns:common.topic.topic_equivalent_webpage sn:.
	?f ns:common.topic.notable_types ?type.
	?type ns:type.object.name	 ?typeid.
	FILTER(LANG(?typeid)='en')
	} 
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results["results"]["bindings"]

import json
import urllib2
from bs4 import BeautifulSoup
import webbrowser
import re
import json
import time
from SPARQLWrapper import SPARQLWrapper, JSON

infile=open('!allwikiid.txt','r')
of=open('wiki_keyword_with_link.txt','w')
num=0
sum=0
sign=0
for line in infile:

	print '###############'
	num+=1
	if line.replace('\n','')=='583407':
		sign=1

	if sign!=1:
		continue
	print bcolors.WARNING+str(sum)+'/'+str(num)+bcolors.ENDC
	print line,
	data={}

	start_url='http://en.wikipedia.org/wiki/index.html?curid='+line.replace('\n','')
	try:
		req = urllib2.Request(start_url, headers={ 'User-Agent': 'Mozilla/5.0' })
		cont = urllib2.urlopen(req).read()
		soup = BeautifulSoup(cont)
	except:
		continue
	 
	print 
	movietitle= soup.find("h1", {"id": "firstHeading"}).text
	data['movie_title']=movietitle
	data['movie_wikiid']=line.replace('\n','')
	data['movie_keywords']=[]
	print data
	try:
		p=soup.find("span", {"id": "Plot"}).parent.find_next_sibling()
	except:
		continue
	alllink=[]
	while p.name=='div':
			#print 1
			p=p.find_next_sibling()
	while p.name=='p':
		#here find all possible links in a plot by looping through the external links, mark the ID
		for a in p.findAll('a'):
			try:
				# handle redirect
				if a['class'] == ['mw-redirect']:
					#print a['class'][0]
					url='https://en.wikipedia.org/w/index.php?title='+a['href'][6:]+'&redirect=no'
					req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
					cont = urllib2.urlopen(req).read()
					soup = BeautifulSoup(cont)
					newtitle = soup.find("ul", {"class": "redirectText"}).find('a')['href'][19:].replace('&redirect=no','')
					#print newtitle
					alllink.append('https://en.wikipedia.org/wiki/'+newtitle)

			except:
				#print
				alllink.append('https://en.wikipedia.org'+a['href'])
			#print a['href']
		p=p.find_next_sibling()
		#print p.name
		while p.name=='div':
			#print 1
			p=p.find_next_sibling()


	
	
	for link in alllink:
		title= link.replace('https','http')[29:]
		print title,
		#freebase_info = wiki_address_to_freebase_info(link.replace('https','http'))
		# print 'Freebase_info:'
		# if len(freebase_info) != 0:
		# 	print 'Type: '+freebase_info[0]['typeid']['value']
		# else:
		# 	print 
		
		sparql_results=wiki_address_to_wiki_info(link.replace('https','http'))

		for info in sparql_results:
			#if info
			print info['wid']['value']
			k_data={}
			k_data['keyword_title']=title
			k_data['value']=info['wid']['value']
			data['movie_keywords'].append(k_data)
			#ttt= info['type']['value']
			#if ttt.startswith('http://dbpedia.org/ontology/') or ttt.startswith('http://dbpedia.org/class/yago/'):
				#print bcolors.WARNING+ttt+bcolors.ENDC
			
			
	#print data
	json.dump(data, of)	
	of.write('\n')
	sum+=1		
	#break
	# a='http://en.wikipedia.org/wiki/Fight_Club'
	# print wiki_address_to_wiki_info(a)

