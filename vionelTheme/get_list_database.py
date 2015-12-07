from pymongo import MongoClient


client = MongoClient('192.168.1.76')
db = client.imdb_usr_list.boxer


def select_dataset():
   """
   Mongodb Fields:

   '_id' - mongodb id
   'usr_id' - you know what this is
   'list_id' - imdb usr list id
   'movie_list_id' - list of imdb movie ids
   'title' - title of the list
   'description' - you know what this is
   
   """
   for row in db.find():
       print "Keys", row.keys()
       print "-" * 10
       print row
       break

select_dataset()