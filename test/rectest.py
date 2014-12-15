from recommender.eval import eval_user
from recommender.metrics import Metrics
import unittest

class TestEval(unittest.TestCase):

	def test_eval_user(self):
		expectedAnswer = dict()
		expectedAnswer['test'] = ['a', 'bc', 'aa']
		self.assertEquals(eval_user('test', [('a',1), ('c',1), ('d',1)], expectedAnswer), 1.0/3)
		self.assertEquals(eval_user('test', [('a',1), ('c',1), ('d',1), ('d',1), ('d',1), ('a',1)], expectedAnswer), 1.0/3)
		
		expectedAnswer['test'] = ['a', 'bc', 'aa', 'd', 'e ', 'f']
		self.assertEquals(eval_user('test', [('a',1), ('c',1), ('d',1)], expectedAnswer), 2.0/5)
		self.assertEquals(eval_user('test', [('a',1), ('c',1), ('d',1), ('d',1), ('5',1), ('a',1)], expectedAnswer), 3.0/5)


class TestMetrics(unittest.TestCase):

	def setUp(self):
		problemA = { 'PROBLEM':'P1', 'RESULT':'AC'}
		problemB = { 'PROBLEM':'P1', 'RESULT':'WC'}
		problemC = { 'PROBLEM':'P2', 'RESULT':'AC'}
		problemD = { 'PROBLEM':'P2', 'RESULT':'WC'}
		
		byUser = dict()
		byUser['u1'] = [problemA, problemA, problemD]
		byUser['u2'] = [problemA, problemB, problemC, problemD]
		byUser['u3'] = [problemB, problemD]
		byUser['u4'] = [problemA, problemC]
		
		self.metrics = Metrics(byUser)

	def test_num_objs(self):
		self.assertEquals(self.metrics.get_num_problems(), 2)
		self.assertEquals(self.metrics.get_num_users(), 4)
		self.assertEquals(self.metrics.get_num_all_submitions(), 11)
	
	
	def test_num_submitions(self):
		self.assertEquals(self.metrics.get_num_submitions('P1'), 6)
		self.assertEquals(self.metrics.get_num_submitions('P2'), 5)
		self.assertEquals(self.metrics.get_num_submitions('P1') + self.metrics.get_num_submitions('P2'), self.metrics.get_num_all_submitions())
	
	
	def test_ac_submitions(self):
		self.assertEquals(self.metrics.get_ac_submitions('P1'), 4)
		self.assertEquals(self.metrics.get_ac_submitions('P2'), 2)
		
		
	def test_distinct_ac_submitions(self):
		self.assertEquals(self.metrics.get_distinct_ac_submitions('P1'), 3)
		self.assertEquals(self.metrics.get_distinct_ac_submitions('P2'), 2)
	
	
	def test_distinct_submitions(self):
		self.assertEquals(self.metrics.get_distinct_submitions('P1'), 4)
		self.assertEquals(self.metrics.get_distinct_submitions('P2'), 4)
	
	
	def test_dacu(self):
		#self.assertEquals(self.metrics.get_dacu('P1'), self.metrics.get_distinct_ac_submitions('P1')/self.metrics.get_distinct_submitions('P1'))
		#self.assertEquals(self.metrics.get_dacu('P2'), self.metrics.get_distinct_ac_submitions('P2')/self.metrics.get_distinct_submitions('P2'))
		self.assertEquals(self.metrics.get_dacu('P1'), self.metrics.get_distinct_ac_submitions('P1'))
		self.assertEquals(self.metrics.get_dacu('P2'), self.metrics.get_distinct_ac_submitions('P2'))
	
	def test_get_distinct_problems(self):
		self.assertEquals(self.metrics.get_problems(), ['P2', 'P1'])


class TestRecommenders(unittest.TestCase):
	def setUp(self):
		problem1 = { 'PROBLEM':'P1', 'RESULT':'AC'}
		problem1r = { 'PROBLEM':'P1', 'RESULT':'WC'}
		problem2 = { 'PROBLEM':'P2', 'RESULT':'AC'}
		problem2r = { 'PROBLEM':'P2', 'RESULT':'WC'}
		problem3 = { 'PROBLEM':'P3', 'RESULT':'AC'}
		problem3r = { 'PROBLEM':'P3', 'RESULT':'WC'}
		problem4 = { 'PROBLEM':'P4', 'RESULT':'AC'}
		problem4r = { 'PROBLEM':'P4', 'RESULT':'WC'}
		problem5 = { 'PROBLEM':'P5', 'RESULT':'AC'}
		problem5r = { 'PROBLEM':'P5', 'RESULT':'WC'}
		problem6 = { 'PROBLEM':'P6', 'RESULT':'AC'}
		problem6r = { 'PROBLEM':'P6', 'RESULT':'WC'}
		
		byUser = dict()
		byUser['u1'] = [problemA, problemA, problemD]
		byUser['u2'] = [problemA, problemB, problemC, problemD]
		byUser['u3'] = [problemB, problemD]
		byUser['u4'] = [problemA, problemC]
		
		self.metrics = Metrics(byUser)
		
		#TODO: NOT IMPLEMENTED YET
		
if __name__ == '__main__':
    unittest.main()
    
