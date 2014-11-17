from operator import itemgetter
from math import sqrt

import logging

from spojrec.src.recommender.database import ProblemsDatabase
from spojrec.src.recommender.metrics import Metrics
from spojrec.src.recommender.eval import eval_user

class Recommender(object):

	def __init__(self, metrics, solvedProblemsByUser):
		self.metrics = metrics
		self.solvedProblemsByUser = solvedProblemsByUser
	
	def get_solved_problems_by_user(self, user):
		return self.solvedProblemsByUser[user]

	def rec(self, user, topk=5):
		raise NotImplementedError


class PopularRec(Recommender):

	def __init__(self, metrics, solvedProblemsByUser):
		super(PopularRec, self).__init__(metrics, solvedProblemsByUser)
		self.problemsSortedByAceptFreq = sorted(metrics.get_problems(), key=lambda problem: metrics.get_num_submitions(problem), reverse=True)
	

	def rec(self, user, topk=5):
		solved = self.get_solved_problems_by_user(user)
		cnt = 0
		rec = []
		
		for problem in self.problemsSortedByAceptFreq:
			if cnt >= topk:
				break
			
			if problem not in solved:
				rec.append((problem, self.metrics.get_num_submitions(problem)))
				cnt += 1
		
		return rec


class AceptRate(Recommender):

	def __init__(self, metrics, solvedProblemsByUser):
		super(AceptRate, self).__init__(metrics, solvedProblemsByUser)
		self.problemsSortedByAceptFreq = sorted(metrics.get_problems(), key=lambda problem: self.compute_acept_freq(problem), reverse=False)
	
	def compute_acept_freq(self, problem):
		return self.metrics.get_ac_submitions(problem)/self.metrics.get_num_submitions(problem)
	
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
	
	def __init__(self, metrics, solvedProblemsByUser):
		super(Dacu, self).__init__(metrics, solvedProblemsByUser)

	
	def compute_user_dacu(self, user, topk=None):
		logging.info('Recommending problems for' + user)
		user_dacu = 0.0
		problems = self.get_solved_problems_by_user(user)
		nump = len(problems)
		
		if topk is not None:
			nump = min(len(problems), topk)
		
		cnt = 0
		for problem in problems:
			if cnt >= nump:
				break
			user_dacu += self.metrics.get_dacu(problem)
			cnt += 1
		
		if nump != 0.0:
			return user_dacu / nump
		
		return self.metrics.get_num_all_submitions()

	
	def rec(self, user, topk=5, numUserProblens=None):
		solved = self.solvedProblemsByUser[user]
		cnt = 0
		rec = []
		
		user_dacu = self.compute_user_dacu(user, numUserProblens)
		
		for problem in self.metrics.get_problems():
			if problem not in solved:
				score = self.metrics.get_dacu(problem)
				rec.append((problem, abs(user_dacu - score)))
		
		ret = []
		for (problem, score) in sorted(rec, key=itemgetter(1)):
			if cnt >= topk:
				break
			
			cnt += 1
			ret.append((problem, score))
		
		return ret

		
class HitsRec(Recommender):

	def __init__(self, metrics, solvedProblemsByUser, steps=5):
		super(HitsRec, self).__init__(metrics, solvedProblemsByUser)
		self.k = steps
		self._comput_hits()
	
	def _comput_hits(self):
		self.hubs = dict()
		self.auth = dict()
		usersByProblems = dict()
		
		for user in self.solvedProblemsByUser:
			self.hubs[user] = 1.0
			self.auth[user] = 1.0
			for problem in self.solvedProblemsByUser[user]:
				if problem not in usersByProblems:
					usersByProblems[problem] = []
				usersByProblems[problem].append(user)
		
		for problem in self.metrics.get_problems():
			self.hubs[problem] = 1.0
			self.auth[problem] = 1.0
			if problem not in usersByProblems:
				usersByProblems[problem] = []
		
		for step in range(self.k):
			self._compute_auth(self.solvedProblemsByUser, usersByProblems, self.auth, self.hubs)
			self._compute_auth(self.solvedProblemsByUser, usersByProblems, self.hubs, self.auth)
	
	
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
	
	
	def rec(self, user, topk=5):
		solved = self.solvedProblemsByUser[user]
		cnt = 0
		rec = []
		
		for problem in self.metrics.get_problems():
			if problem not in solved:
				#score = self.hubs[problem]
				score = 10.0 * self.auth[problem]
				rec.append((problem, abs(self.hubs[user] - score)))
		
		ret = []
		for (problem, score) in sorted(rec, key=itemgetter(1)):
			if cnt >= topk:
				break
			
			cnt += 1
			ret.append((problem, score))
		
		return ret
		
		
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
	
	
