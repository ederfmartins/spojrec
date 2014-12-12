# -*- coding: utf-8 -*-

import sys
from datetime import datetime

ACCEPTED = 'AC'

def sumarise_problems_by_column(allProbs, column):
	ret = dict()
	
	for problem in allProbs:
		if problem[column] not in ret:
			ret[problem[column]] = []
			
		ret[problem[column]].append(problem)
	
	return ret

def sumarize_stats_of_user(uniqueProblems):
	ret = dict()
	ret['attempted'] = len(uniqueProblems)
	ret['solved'] = 0
	ret['failures'] = 0
	ret['accepted_1'] = 0
	ret['most_failures'] = 0
	ret['avg_attempted_per_problem'] = 0
	
	for (problem, attempts) in uniqueProblems.items():
		size = len(attempts)
		ret['avg_attempted_per_problem'] += size
		if attempts[-1]['RESULT'] == ACCEPTED:
			ret['accepted_1'] += 1
		
		nFailures = 0
		for att in attempts:
			if att['RESULT'] != ACCEPTED:
				nFailures += 1
		
		if nFailures != size:
			ret['solved'] += 1
		else:
			ret['failures'] += 1
		
		if ret['most_failures'] < nFailures:
			ret['most_failures'] = nFailures
	
	ret['avg_attempted_per_problem'] = float(ret['avg_attempted_per_problem'])/ret['attempted']
	return ret


def sumarize_submissions_by_month(problems):
	subByMouth = dict()
	
	for prob in problems:
		date = datetime.strptime(prob['DATE'], "%Y-%m-%d %H:%M:%S")
		m = str(date.month)
		
		if date.month < 10:
			m = '0' + m
		
		point = str(date.year) + '/' + m
		
		if point not in subByMouth:
			subByMouth[point] = 0
			
		subByMouth[point] += 1
		
	return subByMouth
	
	
		
