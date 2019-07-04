import msvcrt as m
import time
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from pandas import DataFrame
import matplotlib

import random

class Fuzzy(object):
	
	def __init__(self,lsamarks,wmddistance):

		lsa = ctrl.Antecedent(np.arange(0, 1, 0.1), 'lsa')
		wmd= ctrl.Antecedent(np.arange(0, 1, 0.1), 'wmd')
		final = ctrl.Consequent(np.arange(0, 10, 0.1), 'final')
		lsa.automf(3)
		wmd.automf(3)

		final['low'] = fuzz.trimf(final.universe, [0, 1, 2])
		final['medium'] = fuzz.trimf(final.universe, [2, 4.5, 6])
		final['high'] = fuzz.trimf(final.universe, [6, 8.5, 10])
		
		# lsa.view()
		# time.sleep(5)
		# wmd.view()
		# time.sleep(5)
		
		rule1 = ctrl.Rule(lsa['poor'] & wmd['poor'], final['low'])
		rule2 = ctrl.Rule(lsa['poor'] & wmd['average'], final['low'])
		rule3 = ctrl.Rule(lsa['poor'] & wmd['good'], final['low'])

		rule4 = ctrl.Rule(lsa['average'] & wmd['poor'], final['medium'])
		rule5 = ctrl.Rule(lsa['average'] & wmd['average'], final['high'])
		rule6 = ctrl.Rule(lsa['average'] & wmd['good'], final['high'])

		rule7 = ctrl.Rule(lsa['good'] & wmd['poor'], final['high'])
		rule8 = ctrl.Rule(lsa['good'] & wmd['average'], final['high'])
		rule9 = ctrl.Rule(lsa['good'] & wmd['good'], final['high'])

		final_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
		finalsimulation = ctrl.ControlSystemSimulation(final_ctrl)
		finalsimulation.input['lsa'] = lsamarks
		finalsimulation.input['wmd'] = wmddistance
		finalsimulation.compute()

		# final.view(sim=finalsimulation)
		
		self.final_score = finalsimulation.output['final']
		sum_x = lsamarks + wmddistance*2 
		self.final_score = min(sum_x-random.uniform(0.0,0.1),1)  if sum_x > 0 else 0 
		

	def get_score_data(self):
		return self.final_score

		'''
		{
	  "https://timesofindia.indiatimes.com": "section1",
	  "https://ndtv.com": "ins_storybody",
	  "https://indiatoday.intoday.in": "node-story",
	  "https://indianexpress.com": "o-story-content",
	  "https://thehindu.com": "article",
	  "https://news18.com": "hideCont",
	  "https://auto.ndtv.com" : "article__main"
	}
	'''