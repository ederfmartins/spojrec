# -*- coding: utf-8 -*-

from operator import itemgetter
import logging

from datamodel.database import ProblemsDatabase
from crawler.dataExtractor.signedlistParser import parseSignedlist, LABEL_PROBLEM_COLUMN, LABEL_COLUMN_ACCEPTED
from recommender.util import sumarise_problems_by_column, ACCEPTED

class Recommender(object):

	def __init__(self, metricsDatabase):
		self.metrics = metricsDatabase
		self.problems = self.get_database().get_problems_ids()
	
	def get_database(self):
		return self.metrics
	
	def get_problems(self):
		return self.problems
	
	def get_solved_problems_by_user(self, user):
		subs = self.get_database().get_problems_of_user_from_db(user)
		probs = parseSignedlist(subs['data'])
		if probs is not None:
			p = sumarise_problems_by_column(probs, LABEL_COLUMN_ACCEPTED)
			if ACCEPTED in p:
				return [prob[LABEL_PROBLEM_COLUMN] for prob in p[ACCEPTED]]

		return []
	
	def get_top_recommendations(self, rec, reverse=False, topk=5):
		ret = []
		cnt = 0
		for (problem, score) in sorted(rec, key=itemgetter(1), reverse=reverse):
			if cnt >= topk:
				break
			
			cnt += 1
			ret.append((problem, score))
		
		return ret

	def rec(self, user, topk=5):
		raise NotImplementedError


class PopularRec(Recommender):

	def __init__(self, metrics):
		super(PopularRec, self).__init__(metrics)
		self.problemsSortedByAceptFreq = sorted(self.get_problems(), key=lambda problem: self.get_database().get_acRate(problem), reverse=True)
	

	def rec(self, user, topk=5):
		solved = self.get_solved_problems_by_user(user)
		cnt = 0
		rec = []
		
		for problem in self.problemsSortedByAceptFreq:
			if cnt >= topk:
				break
			
			if problem not in solved:
				rec.append((problem, self.get_database().get_acRate(problem)))
				cnt += 1
		
		return rec


class AceptRate(Recommender):

	def __init__(self, metrics):
		super(AceptRate, self).__init__(metrics)
		self.totalAC = self.get_database().get_totalAC()
		self.problemsSortedByAceptFreq = sorted(self.get_problems(), key=lambda problem: self.compute_acept_freq(problem), reverse=False)
	
	def compute_acept_freq(self, problem):
		return self.get_database().get_acRate(problem)/self.totalAC
	
	def rec(self, user, topk=5):
		solved = self.get_solved_problems_by_user(user)
		cnt = 0.0
		rec = []
		
		for problem in self.problemsSortedByAceptFreq:
			if cnt >= topk:
				break
			
			if problem not in solved:
				rec.append((problem, self.compute_acept_freq(problem)))
				cnt += 1.0
		
		return rec
		

class Dacu(Recommender):
	MAX_DACU = 1000000
	def __init__(self, metrics):
		super(Dacu, self).__init__(metrics)
	
	def get_dacu(self, problem):
		return self.metrics.get_dacu(problem)
	
	def compute_user_dacu(self, problems, topk=None):
		user_dacu = 0.0
		nump = len(problems)
		
		if topk is not None:
			nump = min(len(problems), topk)
		
		problems = sorted(problems, key=lambda problem: self.get_dacu(problem), reverse=False)
		cnt = 0
		for problem in problems:
			if cnt >= nump:
				break
			user_dacu += self.get_dacu(problem)
			cnt += 1
		
		if nump != 0.0:
			return user_dacu / nump
		
		return MAX_DACU
	
	def rec(self, user, topk=5, numUserProblens=None):
		logging.info('Recommending problems for' + user)
		solved = self.get_solved_problems_by_user(user)
		user_dacu = self.compute_user_dacu(solved, numUserProblens)
		rec = []
		
		for problem in self.get_problems():
			if problem not in solved:
				score = self.get_dacu(problem)
				rec.append((problem, abs(user_dacu - score)))
		
		return self.get_top_recommendations(rec, False, topk)

class DacuTopK(Dacu):
	def __init__(self, metrics):
		super(DacuTopK, self).__init__(metrics)
	
	def get_dacu(self, problem):
		return self.metrics.get_topkDacu(problem)

class HitsRec(Recommender):

	def __init__(self, metrics):
		super(HitsRec, self).__init__(metrics)
	
	def rec(self, user, topk=5):
		logging.info('Recommending problems for' + user)
		solved = self.get_solved_problems_by_user(user)
		rec = []
		
		for problem in self.get_problems():
			if problem not in solved:
				#score = self.hubs[problem]
				userHits = self.get_database().get_hits(user)
				probHits = self.get_database().get_hits(problem)
				userScore = userHits['HUBS']
				problemScore = 10.0 * probHits['AUTH']
				rec.append((problem, abs(userScore - problemScore)))
		
		return self.get_top_recommendations(rec, False, topk)
	
