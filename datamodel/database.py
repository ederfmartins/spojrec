# -*- coding: utf-8 -*-
import os
import time
import logging
from operator import isCallable
from pymongo import MongoClient

from crawler.dataExtractor.signedlistParser import parseSignedlist
from constants import MONGODB_URL, MONGODB_USER, MONGODB_PASS, PRODUCTION

class Database(object):
	def __init__(self, contest):
		self._idField = '_id'
		if PRODUCTION:
			self.client = MongoClient(MONGODB_URL)
			self.client.index.authenticate(MONGODB_USER, MONGODB_PASS, mechanism='MONGODB-CR')
			self.db = self.client.index
		else:
			self.client = MongoClient()
			self.db = self.client.index
			#self._idField = 'spojId'

	def get_problems_of_user_from_db(self, spojId):
		submission = self.db.submissionData.find_one({self._idField: spojId})
		if submission is None:
			return None
		
		return submission
	
	def _iterate_over(self, collection, callbackFunc, query=None, *args, **kwargs):
		for obj in collection.find(query).batch_size(100):
			if isCallable(callbackFunc):
				callbackFunc(obj, *args, **kwargs)
	
	def iterate_over_submissions(self, callbackFunc, query=None, *args, **kwargs):
		return self._iterate_over(self.db.submissionData, callbackFunc, query, *args, **kwargs)
	
	def iterate_over_users(self, callbackFunc, query=None, *args, **kwargs):
		return self._iterate_over(self.db.users, callbackFunc, query, *args, **kwargs)
	
	def find_user(self, spojId):
		return self.db.users.find_one({self._idField: spojId})
	
	def find_problem(self, spojId):
		return self.db.problems.find_one({self._idField: spojId})
	
	def update_problem(self, itemAsDict):
		self.db.problems.update({self._idField:itemAsDict[self._idField]}, itemAsDict, upsert=True)
	
	def update_user(self, itemAsDict):
		self.db.users.update({self._idField:itemAsDict[self._idField]}, itemAsDict, upsert=True)
	
	def update_submission_data(self, itemAsDict):
		self.db.submissionData.update({self._idField:itemAsDict[self._idField]}, itemAsDict, upsert=True)

class ProblemsDatabase(Database):
	def __init__(self, contest, loadMetricsOnly=False):
		super(ProblemsDatabase, self).__init__(contest)
		
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
			parsedProblemsByUser[submission['_id']] = problems
		
		return parsedProblemsByUser
	
	
	def _load_metrics(self):
		return self.db.metrics.find_one()
	
	def get_problems_by_user(self):
		return self.parsedProblemsByUser
		
		
	def get_metrics(self):
		if self._metrics is None:
			raise Exception("Metrics not load yet from db!")
		return self._metrics
		
	
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
	
	
class MetricsDatabase(Database):
	def __init__(self, contest):
		super(MetricsDatabase, self).__init__(contest)	
	
	def save_metrics(self, metrics):
		self.db.metrics.insert(metrics.__dict__)
		
	def get_dacu(self, problem):
		obj = self.db.dacu.find_one({self._idField:problem})
		if obj is not None:
			return obj['DACU']
		
		logging.info('Not found dacu for: ' + str(problem))
		return None
	
	def get_topkDacu(self, problem):
		obj = self.db.topkDacu.find_one({self._idField:problem})
		if obj is not None:
			return obj['DACU']
		
		logging.info('Not found dacu for: ' + str(problem))
		return None
	
	def get_acRate(self, problem):
		obj = self.db.acRate.find_one({self._idField:problem})
		if obj is not None:
			return obj['ACRATE']
		return None
	
	def get_totalAC(self, problem):
		obj = self.db.totalAC.find_one({self._idField:'totalAC'})
		if obj is not None:
			return obj['totalAC']
		return None
	
	def get_hits(self, key):
		obj = self.db.hits.find_one({self._idField:key})
		if obj is not None:
			return obj
		return None
	
	def get_problems_size(self):
		return self.db.problems.find().size()
	
	def get_problems_ids(self, query=None):
		ret = []
		for prob in self.db.problems.find(query, {self._idField:1}).batch_size(100):
			ret.append(prob[self._idField])
		return ret
		
	def set_dacu(self, problem, dacu):
		self.db.dacu.update({self._idField:problem}, {self._idField:problem, 'DACU':dacu}, upsert=True)
	
	def set_acRate(self, problem, dacu):
		self.db.acRate.update({self._idField:problem}, {self._idField:problem, 'ACRATE':dacu}, upsert=True)
	
	def set_totalAC(self, value):
		self.db.totalAC.update({self._idField:'totalAC'}, {self._idField:'totalAC', 'totalAC':value}, upsert=True)
	
	def set_hits(self, obj, auth, hubs):
		self.db.hits.update({self._idField:obj}, {self._idField:obj, 'AUTH':auth, 'HUBS':hubs}, upsert=True)
	
	def set_topkDacu(self, prob, probDacu):
		self.db.topkDacu.update({self._idField:prob}, {self._idField:prob, 'DACU':probDacu}, upsert=True)
	
