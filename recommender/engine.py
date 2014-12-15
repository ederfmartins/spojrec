# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta

from constants import DEFAULT_RECOMMENDER
from constants import SPOJ_URLS

from datamodel.database import MetricsDatabase
from recommender.rec import Dacu, HitsRec, DacuTopK
from crawler.util import fetch_user, fetch_problem
from crawler.dataExtractor.signedlistParser import parseSignedlist

def find_user(database, spojId, contest):
    user = database.find_user(spojId)
    if user is None:
        fetch_user(spojId, contest, database)
        user = database.find_user(spojId)
    return user

def find_problem(database, probId, contest):
    theProblem = database.find_problem(probId)
    if (theProblem is None) or ('snippet' not in theProblem):
        fetch_problem(probId, contest, database)
        theProblem = database.find_problem(probId)
    return theProblem

def uptate_problems(database, spojId, contest):
    userProblems = database.get_problems_of_user_from_db(spojId)
            
    if userProblems is None:
        fetch_user(spojId, contest, database, onlySubmitions=True)
        userProblems = database.get_problems_of_user_from_db(spojId)
    else:
        if datetime.utcnow() - userProblems['timestamp'] > timedelta(minutes = 15):
            fetch_user(spojId, contest, database, onlySubmitions=True)
            userProblems = database.get_problems_of_user_from_db(spojId)

def rec(spojId, contest, level, topk=5):
    database = MetricsDatabase(contest)
    problem = database.find_problem(spojId)
    
    if problem is not None:
        pass
    else:
        user = find_user(database, spojId, contest)
            
        if user is not None:
            recommendedProblems = []
            uptate_problems(database, spojId, contest)
		    
            if level == 'Facil':
                rec = Dacu(database)
                recProblems = rec.rec(spojId, topk)
            elif level == 'Normal':
                rec = HitsRec(database)
                recProblems = rec.rec(spojId, topk)
            elif level == 'Dificil':
                rec = DacuTopK(database)
                recProblems = rec.rec(spojId, topk)
		        
            cnt = 0
            for (problem, score) in recProblems:
                if cnt >= topk:
                    break
		        
                theProblem = find_problem(database, problem, contest)
                title = problem
                url = SPOJ_URLS[contest] + problem
                snippet = ''
                if theProblem is not None:
                    title = theProblem['title']
                    if isinstance(title, list):
                        title = ''.join(title)
                    
                    url = theProblem['url']
                    snippet = theProblem['snippet']
                    if isinstance(snippet, list):
                        snippet = ''.join(snippet)
                    
                    snippet = snippet[0 : min(len(snippet), 400)]

                recommendedProblems.append({'spojId':problem, 'url':url, 'title':title, 'snippet':snippet})
                cnt += 1
		    
            return recommendedProblems
		    
    return []

