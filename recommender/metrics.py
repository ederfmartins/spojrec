# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from math import sqrt

from datamodel.database import MetricsDatabase
from crawler.dataExtractor.signedlistParser import parseSignedlist, LABEL_PROBLEM_COLUMN, LABEL_COLUMN_ACCEPTED
from recommender.util import sumarise_problems_by_column, ACCEPTED
from recommender.rec import Dacu
		
class DacuComputation(object):
	def __init__(self, database):
		self.database = database
	
	def process_submission(self, submission, dacus):
		subDict = parseSignedlist(submission['data'])
		probs = sumarise_problems_by_column(subDict, LABEL_COLUMN_ACCEPTED)
		try:
			distinctProbs = set([x[LABEL_PROBLEM_COLUMN] for x in probs[ACCEPTED]])
		except:
			print submission['_id'], probs
		
		for prob in distinctProbs:
			dacus[prob] += 1
	
	def execute(self):
		dacu = defaultdict(int)
		self.database.iterate_over_submissions(self.process_submission, query=None, dacus=dacu)
		
		for (prob, value) in dacu.items():
			self.database.set_dacu(prob, value)

class ACRateComputation(object):
	def __init__(self, database):
		self.database = database
		self.totalAcc = 0
	
	def process_submission(self, submission, acRate):
		subDict = parseSignedlist(submission['data'])
		probs = sumarise_problems_by_column(subDict, 'RESULT')
		
		cnt = 0
		for prob in probs[ACCEPTED]:
			acRate[prob['PROBLEM']] += 1
			cnt += 1
		
		self.totalAcc += cnt
	
	def execute(self):
		self.totalAcc = 0
		acRate = defaultdict(int)
		self.database.iterate_over_submissions(self.process_submission, query=None, acRate=acRate)
		self.database.set_totalAC(self.totalAcc)
		
		for (prob, value) in acRate.items():
			self.database.set_acRate(prob, value)
	
class HitsComputation(object):
	def __init__(self, database, steps=5):
		self.database = database
		self.k = steps
		self.hubs = dict()
		self.auth = dict()
		self.solvedProblemsByUser = dict()
		self.usersByProblems = dict()
	
	def process_submission(self, submission):
		user = submission['_id']
		subDict = parseSignedlist(submission['data'])
		probs = sumarise_problems_by_column(subDict, 'RESULT')
		distinctProbs = set([x['PROBLEM'] for x in probs[ACCEPTED]])
		
		self.solvedProblemsByUser[user] = distinctProbs
		self.hubs[user] = 1.0
		self.auth[user] = 1.0
		
		for problem in distinctProbs:
			if problem not in self.usersByProblems:
				self.usersByProblems[problem] = []
				self.hubs[problem] = 1.0
				self.auth[problem] = 1.0
			self.usersByProblems[problem].append(user)
	
	def execute(self):
		self.database.iterate_over_submissions(self.process_submission, query=None)
		
		for step in range(self.k):
			self._compute_auth(self.solvedProblemsByUser, self.usersByProblems, self.auth, self.hubs)
			self._compute_auth(self.solvedProblemsByUser, self.usersByProblems, self.hubs, self.auth)
		
		for (obj, auth) in self.auth.items():
			self.database.set_hits(obj, auth, self.hubs[obj])
	
	
	def _acumulate_hits(self, G, auth, hub):
		norm = 0.0
		for vertice in G:
			auth[vertice] = 0.0
			for link in G[vertice]: #links that point to vertice
				auth[vertice] += hub[link]
			norm += auth[vertice] * auth[vertice]
		return norm
	
	
	def _compute_auth(self, G, G1, auth, hubs):
		norm = self._acumulate_hits(G, auth, hubs)
		norm += self._acumulate_hits(G1, auth, hubs)
		norm = sqrt(norm)
		for (v, score) in auth.items():
			auth[v] = score/norm

class DacuTopKComputation(object):
	def __init__(self, database, topk):
		self.database = database
		self.topk = topk
		self.usersByProblems = {}
		self.dacuRec = Dacu(database)
		self.dacu = {}
	
	def compute_problem_dacu(self, users):
		prob_dacu = 0.0
		nump = len(users)
		
		if self.topk is not None:
			nump = min(len(users), self.topk)
		
		users = sorted(users, key=lambda user: self.dacu[user], reverse=True)
		cnt = 0
		for user in users:
			if cnt >= nump:
				break
			prob_dacu += self.dacu[user]
			cnt += 1
		
		if nump != 0.0:
			return prob_dacu / nump
		
		return self.dacuRec.MAX_DACU
	
	def process_submission(self, submission):
		user = submission['_id']
		subDict = parseSignedlist(submission['data'])
		probs = sumarise_problems_by_column(subDict, 'RESULT')
		distinctProbs = set([x['PROBLEM'] for x in probs[ACCEPTED]])
		self.dacu[user] = self.dacuRec.compute_user_dacu(distinctProbs, self.topk)
		
		for problem in distinctProbs:
			if problem not in self.usersByProblems:
				self.usersByProblems[problem] = []
			self.usersByProblems[problem].append(user)
	
	def execute(self):
		self.database.iterate_over_submissions(self.process_submission, query=None)
		
		for (prob, listUsers) in self.usersByProblems.items():
			probDacu = self.compute_problem_dacu(listUsers)
			self.database.set_topkDacu(prob, probDacu)


def compute_metrics(contest):
	print 'load problems database'
	database = MetricsDatabase(contest)
	print 'calc dacu'
	DacuComputation(database).execute()
	print 'calc dacu top 10'
	DacuTopKComputation(database, 10).execute()
	print 'calc acc rate'
	ACRateComputation(database).execute()
	print 'calc hits'
	HitsComputation(database).execute()

if __name__ == "__main__":
	contest = sys.argv[1]
	compute_metrics(contest)

