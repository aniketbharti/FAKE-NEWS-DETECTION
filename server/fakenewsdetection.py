from googlesearch import search

from sumy.parsers.plaintext import PlaintextParser #summmarization package
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.text_rank import TextRankSummarizer

import json , numpy as np

from bs4 import BeautifulSoup #scarping html

from requests import get #web content getter
from requests.exceptions import RequestException
from contextlib import closing # close all open connection if any

from lsa import LSA 
from wordmover import WordMoverDistance 
from fuzzy import Fuzzy

class FakeNewDetection(object):
	
	def __init__(self):
		with open('search-website.json') as f:
			self.data = json.load(f)
	
	def articleSummerization(self,article,length):

		parser = PlaintextParser.from_string(article, Tokenizer("english"))
		stemmer = Stemmer("english")
		summarizer = TextRankSummarizer(stemmer)
		summarizer.stop_words = get_stop_words("english")
		return ' '.join([ str(i) for i in summarizer(parser.document,length)])
	
	def googleSearch(self, query):
		self.scrapSites = []
		self.scrapId = []
		try :
			for j in search(query, tld="com", num=40, start=0, stop=40, pause=1):
				# print(j)
				for news, scrapId in self.data.items(): #check wheheter link is in the apna serach_websites json
					# print(news,j)
					if news in j:
						# print('aaya\n')
						self.scrapSites.append(j)
						self.scrapId.append(scrapId)
					else:
						pass
						# print('nahi aaya\n')

			return self.scrapSites, self.scrapId

		except Exception as e:
			print(e)
			return 0,[]
	
	def simple_get(self,url):
		try:
			with closing(get(url, stream=True)) as resp:
				if self.is_good_response(resp):
					return resp.content
				else:
					return None
		except RequestException as e:
			self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
			
	def is_good_response(self,resp):
		content_type = resp.headers['Content-Type'].lower()
		return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
	
	def log_error(self,e):
		print(e)

	def initialize(self,article):

		similarity_array = []
		# similarity_array.append(article)
		test = self.articleSummerization(article,1) # in one line

		# for i in summerizedSentence:
		# 	test=str(i)
		print('-------Summerized Title-------')
		print(test)

		sitesContainingArticle, scrapId = self.googleSearch(article)

		print('sites_length_after_google search',len(sitesContainingArticle))

		for index, url in enumerate(sitesContainingArticle):
			print('URL ',url,scrapId[index],'\n')

			raw_html = self.simple_get(url) #full page site content 
			try :
				soup = BeautifulSoup(raw_html, 'html.parser') #proper formattinh raw_html
				# print('hua idhar')
				# print(soup)

			except Exception as e:
				print(e)
				return 0 , []

			_ = [s.extract() for s in soup('script')]

			soup_article = soup.find_all('div', {"class": scrapId[index]})

			# print(soup_article)

			article_string=''
			for data in soup_article:
				# print(data)
				article_string += data.text
				# article_string += data.text   
			# print(article_string)
			if not article_string == '':
				# print('aaya\n')
				similarity_array.append(self.articleSummerization(article_string,5))

			else:
				print('nahi aaya\n')
				pass

		# for c in similarity_array:
		# 	print('\n\n\n',c)

		mylsa = LSA()
		wmdinit = WordMoverDistance()

		length = len(similarity_array)
		# print(length)

		if length == 0:
			return 0 , sitesContainingArticle
		else:
			count = 0
			score_array=[]

			while (count<length):
				print('\n\n',similarity_array[count])
				lsa_similarity = mylsa.start([article+' '+article]+similarity_array,count+1)
				wmdinit.data_accept(similarity_array[count],article)
				wmddistance = wmdinit.model()
			
				print('wordmover distance is',wmddistance)


				fuzzy = Fuzzy(lsa_similarity,wmddistance)
				score = fuzzy.get_score_data()
				# score = score/10
				print('final score ',score)

				score_array.append(score)
				count = count + 1

			score_array = sorted(score_array,key=lambda x:x,reverse=True)

			return min(100, np.around(sum(score_array[:2]),decimals=2)*100 ), sitesContainingArticle
# wmdinit=wordmover.WordMoverDistance(titles[count],titles[0])
# wmddistance=wmdinit.model()