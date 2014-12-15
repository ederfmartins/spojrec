# -*- coding: utf-8 -*-
from operator import itemgetter
from math import sqrt

import logging

from datamodel.database import ProblemsDatabase
from recommender.metrics import Metrics
from recommender.eval import eval_user
from crawler.dataExtractor.signedlistParser import parseSignedlist
from recommender.util import sumarise_problems_by_column, ACCEPTED
		
		
def get_acepted_problems(problemsByUser):
	aceptedProblems = dict()
	
	for (user, problems) in problemsByUser.items():
		aceptedProblems[user] = set(x['PROBLEM'] for x in problems if x['RESULT'] == 'AC')
	
	return aceptedProblems

def get_attempted_problems(problemsByUser):
	aceptedProblems = dict()
	
	for (user, problems) in problemsByUser.items():
		aceptedProblems[user] = list(x['PROBLEM'] for x in problems)
	
	return aceptedProblems

if __name__ == "__main__":
	def _test(test, dacu, aceptRate, popularRec, hits):
		meanDacu = 0.0
		meanDacuLastProb = 0.0
		meanCommons = 0.0
		meanAceptRate = 0.0
		meanrecHits = 0.0
		topk = 5
		expectedAnswer = get_attempted_problems(database.get_expected_answer())
	
		for user in test:
			recCommons = popularRec.rec(user, topk)
			meanCommons += eval_user(user, recCommons, expectedAnswer)
		
			recDacu = dacu.rec(user, topk)
			meanDacu += eval_user(user, recDacu, expectedAnswer)
		
			recDacuLastProbs = dacu.rec(user, topk, 10)
			meanDacuLastProb += eval_user(user, recDacuLastProbs, expectedAnswer)
		
			recAceptRate = aceptRate.rec(user, topk)
			meanAceptRate += eval_user(user, recAceptRate, expectedAnswer)
			
			recHits = hits.rec(user, topk)
			meanrecHits += eval_user(user, recHits, expectedAnswer)
	
		print 'rec_most_commons', 'rec_dacu', 'rec_dacu_last_probs', 'rec_acept_rate', 'hits'
		print meanCommons/len(test), meanDacu/len(test), meanDacuLastProb/len(test), meanAceptRate/len(test), meanrecHits/len(test)
		
	
	database = ProblemsDatabase()
	metrics = Metrics(database.get_test())
	test = get_acepted_problems(database.get_test())
	
	dacu = Dacu(metrics, test)
	aceptRate = AceptRate(metrics, test)
	popularRec = PopularRec(metrics, test)
	hits = HitsRec(metrics, test)
	
	print hits.auth['ederfmartins'], hits.hubs['ederfmartins']
	print hits.rec('ederfmartins')
	print hits.auth['dilsonguim'], hits.hubs['dilsonguim']
	print hits.rec('dilsonguim')
	
	#print dacu.compute_user_dacu('ederfmartins')
	#print dacu.rec('ederfmartins')
	#print dacu.compute_user_dacu('dilsonguim')
	#print dacu.rec('dilsonguim')
	_test(test, dacu, aceptRate, popularRec, hits)

