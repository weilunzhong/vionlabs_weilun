from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import wordpunct_tokenize

# stop = set(stopwords.words('english'))
# stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '-', '&'])
# # print stop
# sentence = "the NOT-so-great-but-still-enjoyable list of gay-themed movies"
# # stemmer = PorterStemmer()

# stemmer = SnowballStemmer("english")

# # wordpunct_tokenize(doc)

# removed = [i.lower() for i in wordpunct_tokenize(sentence) if i.lower() not in stop]


# singles = [stemmer.stem(word) for word in removed]
# print singles

class TitlePreprocesser(object):

	def __init__(self, title):
		self.title = title

	def stop_word_removal(self):
		stop_words = set(stopwords.words("english"))
		stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '-', '&'])
		self.title_removed = [i.lower() for i in wordpunct_tokenize(self.title) if i.lower() not in stop_words]

	def stemming(self):
		stemmer = SnowballStemmer("english")
		self.title_stem = [stemmer.stem(word) for word in self.title_removed]


class KeywordNGram(object):

	def __init__(self, title_stemmed):
		self.title_stemmed = title_stemmed
		self.title_length = len(self.title_stemmed)

	def bi_gram(self):
		self.bi_gram_keywords = []
		for i in range(0,self.title_length-1):
			self.bi_gram_keywords.append(self.title_stemmed[i] + ' ' + self.title_stemmed[i+1])

	def tri_gram(self):
		



TP = TitlePreprocesser("the NOT-so-great-but-still-enjoyable list of gay-themed movies")
TP.stop_word_removal()
TP.stemming()

KNG = KeywordNGram(TP.title_stem)
KNG.bi_gram()
print TP.title_stem
print KNG.bi_gram_keywords