# -*- coding: utf-8 -*-

import sys
import subprocess
from operator import itemgetter
from subprocess import PIPE
from collections import defaultdict

from datamodel.database import Database
from crawler.dataExtractor.signedlistParser import parseSignedlist

def write_plot(plotName, xlabel, ylabel, title, maxX, lineTipe):
	with open(plotName + '.plot', 'w') as f:
		print >>f, 'set xlabel "' + xlabel + '"'
		print >>f, 'set xrange [0:' + str(maxX) + ']'
		print >>f, 'set ylabel "' + ylabel + '"'
		print >>f, 'set key off'
		print >>f, 'set xtics auto'
		print >>f, 'set pointsize 2'
		print >>f, 'set terminal postscript eps enhanced "Helvetica" 28'
		print >>f, 'set output "' + plotName + '.eps"'
		print >>f, 'plot "' + plotName + '.dat" using 1:2 title "' + title + '" with ' + lineTipe

def gen_solved_dist_prob(contest, plotName):
	ACCEPTED_CNT = dict()
	def _sumarize_user(submissions):
		problems = parseSignedlist(submissions['data'])
		accepted = set(x['PROBLEM'] for x in problems if x['RESULT'] == 'AC')
		size = len(accepted)
		
		if size not in ACCEPTED_CNT:
			ACCEPTED_CNT[size] = 0
		
		ACCEPTED_CNT[size] += 1		
	
	database = Database(contest)
	database.iterate_over_submissions(_sumarize_user)
	with open(plotName + '.dat', 'w') as f:
		print >>f, '# <num solved> <num users>'
		for numSolved in ACCEPTED_CNT:
			print >>f, numSolved, ACCEPTED_CNT[numSolved]
	
	write_plot(plotName, "problemas", "# users", "Solved problems dist", 100, 'impulses')
	print subprocess.Popen("gnuplot <" + plotName + ".plot", shell=True, stdout=PIPE).stdout.read()	


DACU = defaultdict(int)
MEAN_DACU = defaultdict(float)
idField = 'spojId'

def _sumarize_dacu(submissions):
	problems = parseSignedlist(submissions['data'])
	accepted = set(x['PROBLEM'] for x in problems if x['RESULT'] == 'AC')
	
	for prob in accepted:
		DACU[prob] += 1

def _sumarize_mean_dacu(submissions):
	problems = parseSignedlist(submissions['data'])
	accepted = set(x['PROBLEM'] for x in problems if x['RESULT'] == 'AC')

	for prob in accepted:
		MEAN_DACU[submissions[idField]] += DACU[prob]
	
	if len(accepted) == 0:
		MEAN_DACU[submissions[idField]] = 10000
	else:
		MEAN_DACU[submissions[idField]] /= len(accepted)

def _sumarize_mean_top_dacu(submissions, topk):
	problems = parseSignedlist(submissions['data'])
	accepted = set(x['PROBLEM'] for x in problems if x['RESULT'] == 'AC')
	dacu = [(x, DACU[x]) for x in accepted]
	cnt = 0
	for (prob, dacu) in sorted(dacu, key=itemgetter(1), reverse=False):
		if cnt >= topk:
			break
		MEAN_DACU[submissions[idField]] += dacu
		cnt += 1
	
	if len(accepted) == 0:
		if idField in submissions:
			MEAN_DACU[submissions[idField]] = 10000
		else:
			print >>sys.stderr, idField + ' not found at: ' + str(submissions)
	else:
		MEAN_DACU[submissions[idField]] /= topk
		
def gen_dacu_dist_prob(contest, plotName):	
	database = Database(contest)
	database.iterate_over_submissions(_sumarize_dacu)
	with open(plotName + '.dat', 'w') as f:
		print >>f, '# <prob> <dacu> <prob name>'
		cnt = 0
		for (prob, dacu) in sorted(DACU.items(), key=itemgetter(1), reverse=True):
			print >>f, cnt, dacu, prob
			cnt += 1
	
	write_plot(plotName, "Problema", "DACU", "DACU dist", 500, 'impulses')
	print subprocess.Popen("gnuplot <" + plotName + ".plot", shell=True, stdout=PIPE).stdout.read()


def gen_dacu_per_user(contest, plotName, sumarizeFunc, *args, **kwargs):
	database = Database(contest)
	database.iterate_over_submissions(_sumarize_dacu)
	database.iterate_over_submissions(sumarizeFunc, None, *args, **kwargs)
	with open(plotName + '.dat', 'w') as f:
		print >>f, '# <prob> <dacu> <user>'
		cnt = 0
		for (user, dacu) in sorted(MEAN_DACU.items(), key=itemgetter(1), reverse=True):
			print >>f, cnt, dacu, user
			cnt += 1
	
	write_plot(plotName, "Users", "Mean DACU", "Mean DACU per user", 13000, 'impulses')
	print subprocess.Popen("gnuplot <" + plotName + ".plot", shell=True, stdout=PIPE).stdout.read()

def gen_dacu_vs_prob_count(contest, plotName, sumarizeFunc, *args, **kwargs):
	database = Database(contest)
	database.iterate_over_submissions(_sumarize_dacu)
	database.iterate_over_submissions(sumarizeFunc, None, *args, **kwargs)
	with open(plotName + '.dat', 'w') as f:
		print >>f, '# <# problems> <dacu> <user>'
		for (user, dacu) in sorted(MEAN_DACU.items(), key=itemgetter(1), reverse=True):
			subOfUser = database.get_problems_of_user_from_db(user)
			if subOfUser is not None:
				subs = parseSignedlist(subOfUser['data'])
				accepted = set(x['PROBLEM'] for x in subs if x['RESULT'] == 'AC')
				print >>f, len(accepted), dacu, user
			else:
				print sys.stderr, user + ' not found'
	
	write_plot(plotName, "Prob count", "DACU", "DACU vs prob count", 13000, 'points')
	print subprocess.Popen("gnuplot <" + plotName + ".plot", shell=True, stdout=PIPE).stdout.read()

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print >>sys.stderr, 'usage: <func name> <contest name> <plot name>'
		exit(-1)
	
	funcName = sys.argv[1]
	contest = sys.argv[2]
	plotName = sys.argv[3]
	
	if funcName == 'solved_dist_prob':
		gen_solved_dist_prob(contest, plotName)
	elif funcName == 'dacu':
		gen_dacu_dist_prob(contest, plotName)
	elif funcName == 'user_dacu':
		gen_dacu_per_user(contest, plotName, _sumarize_mean_dacu)
	elif funcName == 'user_dacu_top':
		gen_dacu_per_user(contest, plotName, _sumarize_mean_top_dacu, int(sys.argv[4]))
	elif funcName == 'dacu_vs_prob_count':
		gen_dacu_vs_prob_count(contest, plotName, _sumarize_mean_top_dacu, int(sys.argv[4]))

