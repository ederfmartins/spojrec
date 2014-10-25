
from collections import defaultdict

from rectest.database import ProblemsDatabase
from eval import eval_user

class Metrics(object):

	def __init__(self, problems):
		self.parsedProblemsByUser = problems
		self._compute_metrics()
	
	def _compute_metrics(self):
		self._compute_num_submissions()
		self._compute_acept_submissions()
		self._compute_problems()

	def _compute_num_submissions(self):
		self.problemsSub = defaultdict(float)
		self.distinctProblemsSub = defaultdict(float)
		self.allSub = 0.0
		
		for (user, problems) in self.parsedProblemsByUser.items():
			probs = defaultdict(float)
			for problem in problems:
				probs[problem['PROBLEM']] += 1.0
				self.allSub += 1.0
			
			for problem in probs:
				self.problemsSub[problem] += probs[problem]
				self.distinctProblemsSub[problem] += 1.0
				

	def _compute_acept_submissions(self):
		self.problemsAcept = defaultdict(float)
		self.distinctProblemsAcept = defaultdict(float)
		
		for (user, problems) in self.parsedProblemsByUser.items():
			probs = defaultdict(float)
			for problem in problems:
				if problem['RESULT'] == 'AC':
					probs[problem['PROBLEM']] += 1.0
			
			for problem in probs:
				self.problemsAcept[problem] += probs[problem]
				self.distinctProblemsAcept[problem] += 1.0
		
	
	def _compute_problems(self):
		self.problems = [x for x in self.distinctProblemsSub]
	
	
	def get_problems(self):
		return self.problems
	
	def get_distinct_problems(self):
		return self.distinctProblemsSub
		
	def get_num_all_submitions(self):
		return self.allSub
	
	def get_num_problems(self):
		return len(self.problemsSub)
	
	def get_num_users(self):
		return len(self.parsedProblemsByUser)
	
	def get_num_submitions(self, problem):
		return self.problemsSub[problem]
	
	def get_ac_submitions(self, problem):
		return self.problemsAcept[problem]
	
	def get_distinct_submitions(self, problem):
		return self.distinctProblemsSub[problem]
	
	def get_distinct_ac_submitions(self, problem):
		return self.distinctProblemsAcept[problem]
	
	def get_dacu(self, problem):
		if problem not in self.distinctProblemsSub:
			raise ValueError(str(problem) + " not found in metrics database.")
		#return self.distinctProblemsAcept[problem]/self.distinctProblemsSub[problem]
		return self.distinctProblemsAcept[problem]	
		


