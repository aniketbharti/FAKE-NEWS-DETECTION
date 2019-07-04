from time import time
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk import download
from gensim.similarities import WmdSimilarity
from nltk import word_tokenize
import os

class WordMoverDistance (object):

	def __init__(self):
		self.stopwords = [] 
		with open('stopwords.txt') as my_file:
			for line in my_file:
				self.stopwords.append(line[:-1])
	
	def data_accept(self,check_article,reffer_article):
		self.check_article = self.preprocess(check_article.lower().split())
		self.reffer_article = self.preprocess(reffer_article.lower().split())

	def preprocess(self, doc):
		doc = [w for w in doc if not w in self.stopwords]  # Remove stopwords.
		doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
		return doc

	def model(self):
		
		if not os.path.exists('GoogleNews-vectors-negative300-SLIM.bin'):
			raise ValueError("SKIP: You need to download the google news model")
		model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)
		model.init_sims(replace=True)  # Normalizes the vectors in the word2vec class.
		distance = model.wmdistance(self.check_article, self.reffer_article)
		if distance > 1:
			return 0
		return (1-distance)








