
import os
import time
from pymongo import MongoClient
from spojrec.src.crawler.crawler.dataExtractor.signedlistParser import parseSignedlist

from constants import MONGODB_URL, MONGODB_USER, MONGODB_PASS

class ProblemsDatabase(object):
	def __init__(self, loadMetricsOnly=False):
		PRODUCTION = True
		
		if PRODUCTION:
			self.client = MongoClient(MONGODB_URL)
			self.client.index.authenticate(MONGODB_USER, MONGODB_PASS, mechanism='MONGODB-CR')
			self.db = self.client.index
		else:
			self.client = MongoClient()
			self.db = self.client.spojrec
		
		if loadMetricsOnly:
			self._metrics = self._load_metrics()
		else:
			self.parsedProblemsByUser = self.load_problems()
			print 'estou vivo'
			if not PRODUCTION:
				self._split(self.parsedProblemsByUser)
	
	
	def load_problems(self):
		parsedProblemsByUser = dict()
		
		cnt = 0
		for submission in self.db.submissionData.find().batch_size(100):
			cnt += 1
			if cnt %100 == 0:
				print 'parsing', cnt
				
			problems = [{"PROBLEM" : pp['PROBLEM'], 'RESULT':pp['RESULT']} for pp in parseSignedlist(submission['data'])]
			parsedProblemsByUser[submission['spojId']] = problems
		
		return parsedProblemsByUser
	
	
	def get_problems_of_user_from_db(self, spojId):
		submission = self.db.submissionData.find_one({"spojId": spojId})
		ret = dict()
		ret[spojId] = parseSignedlist(submission['data'])
		return ret
	
	def save_metrics(self, metrics):
		self.db.metrics.insert(metrics.__dict__)
	
	
	def _load_metrics(self):
		return self.db.metrics.find_one()
	
	
	def get_metrics(self):
		if self._metrics is None:
			raise Exception("Metrics not load yet from db!")
		return self._metrics
	
	
	def find_user(self, spojId):
		return self.db.users.find_one({"spojId": spojId})
	
	
	def find_problem(self, spojId):
		return self.db.problems.find_one({"spojId": spojId})
		
	
	def _find_expected_answer(self, problems):
		cnt = 0
		idx = 0
		for problem in problems:
			if problem['RESULT'] == 'AC':
				idx = cnt
				if idx >= 10:
					return idx
			
			cnt += 1
		
		return 0
			
		
	def _split(self, parsedProblemsByUser):
		self.expectedAnswer = dict()
		self.test = dict()
		
		for user in parsedProblemsByUser:
			idx = self._find_expected_answer(parsedProblemsByUser[user])
			if idx >= 10:
				self.expectedAnswer[user] = parsedProblemsByUser[user][0:idx]
				self.test[user] = parsedProblemsByUser[user][idx:]
	
	def get_expected_answer(self):
		return self.expectedAnswer
		
		
	def get_test(self):
		return self.test
	
	
	def get_problems_by_user(self):
		return self.parsedProblemsByUser
	
