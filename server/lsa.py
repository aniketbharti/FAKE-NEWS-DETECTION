from numpy import zeros
from scipy.linalg import svd
import math
from math import log
from numpy import asarray, sum
import numpy as np
import os, fnmatch
import time
from porter2stemmer import Porter2Stemmer

start_time = time.time()

class LSA(object):
	def __init__(self):
		self.stopwords = []
		self.stemmer = Porter2Stemmer()
		with open('stopwords.txt') as my_file:
			for line in my_file:
				self.stopwords.append(self.stemmer.stem(line[:-1]))
		self.ignorechars = ''',:'!()''' 
		
	
	def start(self,similarity_array,index):
		self.wdict = {} 
		self.dcount = 0
		for article in similarity_array:
			self.parse(article)
			self.build()
			#self.TFIDF()
		print ("word matrix \n")
		self.printA()
		self.calc(index)
		print ("word matrix after normalization \n")
		self.printA()

		self.m=self.cos_sim(self.D,self.M)
		self.ans=(100-(math.degrees(math.acos(self.m))*10)/9)/100
		if self.ans<=0:
			self.ans=0
		print("Your LSA Marks is",self.ans)
		return self.ans		

	def parse(self, doc):
		words = doc.split()
		for w in words:
			w = w.lower().translate(self.ignorechars)
			# print(w)
			w = self.stemmer.stem(w)
			if w in self.stopwords:
				continue
			elif w in self.wdict:
				self.wdict[w].append(self.dcount)
			else:
				self.wdict[w] = [self.dcount]
		self.dcount += 1


	def build(self):
		self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1] 
		self.keys.sort() 
		self.A = zeros([len(self.keys), self.dcount]) 
		for i, k in enumerate(self.keys):
			for d in self.wdict[k]:
				self.A[i,d] += 1


	def TFIDF(self):
		WordsPerDoc = sum(self.A, axis=0)
		DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
		rows, cols = self.A.shape
		for i in range(rows):
			for j in range(cols):
				self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

	def calc(self,c):
		self.U, self.S, self.Vt = svd(self.A,full_matrices=False)
		self.S=np.diag(self.S)
		self.k=self.U.dot(self.S)
		self.A=self.k.dot(self.Vt)
		self.D=[]
		self.M=[]
		for i in self.A:
			self.D.append(i[0])	
		for i in self.A:
			self.M.append(i[c])

	def printA(self):
		print (self.A)
		print("\n")

	def cos_sim(self,a, b):
		dot_product = np.dot(a, b)
		norm_a = np.linalg.norm(a)
		norm_b = np.linalg.norm(b)
		return dot_product / (norm_a * norm_b)

