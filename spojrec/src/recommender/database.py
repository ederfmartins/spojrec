
from crawler.crawler.dataExtractor.signedlistParser import parseSignedlist

#from pymongo import MongoClient

class ProblemsDatabase(object):
	def __init__(self):
		#self.client = MongoClient()
		self.db = self.client.spojrec
		
		self.parsedProblemsByUser = self.load_problems()
		self._split(self.parsedProblemsByUser)
	
	
	def load_problems(self):
		parsedProblemsByUser = dict()
		
		for submission in self.db.submissionData.find():
			parsedProblemsByUser[submission['spojId']] = parseSignedlist(submission['data'])
		
		return parsedProblemsByUser
	
	
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
	
