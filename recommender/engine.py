# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta

from constants import DEFAULT_RECOMMENDER
from constants import SPOJ_URLS

from datamodel.database import ProblemsDatabase
from recommender.rec import Dacu, HitsRec, get_acepted_problems
from recommender.metrics import Metrics
from crawler.util import fetch_user, fetch_problem
from crawler.dataExtractor.signedlistParser import parseSignedlist

def create_default_recommender():
    print 'load problems database'
    database = ProblemsDatabase('BR', False)
    print 'calc metrics'
    metrics = Metrics(database.get_problems_by_user())
    print 'save metrics'
    database.save_metrics(metrics)


def rec(spojId, contest, level, recName='DACU',topk=5):
    database = ProblemsDatabase(contest, True)
    metricsDict = database.get_metrics()

    if spojId in metricsDict["problems"]:
        pass
    else:
        user = database.find_user(spojId)
        if user is None:
            fetch_user(spojId, contest, database)
            user = database.find_user(spojId)
            
        if user is not None:
            metrics = Metrics()
            metrics.__dict__.update(metricsDict)
            recommendedProblems = []
            userProblems = database.get_problems_of_user_from_db(spojId)
            
            if userProblems is None:
                fetch_user(spojId, contest, database, onlySubmitions=True)
                userProblems = database.get_problems_of_user_from_db(spojId)
            else:
                if datetime.utcnow() - userProblems['timestamp'] > timedelta(minutes = 15):
                    fetch_user(spojId, contest, database, onlySubmitions=True)
                    userProblems = database.get_problems_of_user_from_db(spojId)
		    
            probByUser = dict()
            probByUser[spojId] = parseSignedlist(userProblems['data'])
            probs = get_acepted_problems(probByUser)
		    
            if recName == 'DACU':
                rec = Dacu(metrics, probs)
                recProblems = rec.rec(spojId, topk)
            elif recName == 'HITS':
                rec = HitsRec(metrics, probs)
                recProblems = rec.rec(spojId, topk)
		        
            cnt = 0
            for (problem, score) in recProblems:
                if cnt >= topk:
                    break
		        
                theProblem = database.find_problem(problem)
                if theProblem is None:
                    fetch_problem(problem, contest, database)
                    theProblem = database.find_problem(problem)
                title = problem
                url = SPOJ_URLS[contest] + problem
                snippet = ''
                if theProblem is not None:
                    title = theProblem['title']
                    if isinstance(title, list):
                        title = ''.join(title)
                    
                    url = theProblem['url']
                    if 'snippet' not in theProblem:
                        fetch_problem(problem, contest, database)
                        theProblem = database.find_problem(problem)
                    
                    snippet = theProblem['snippet']
                    if isinstance(snippet, list):
                        snippet = ''.join(snippet)
                    
                    snippet = snippet[0 : min(len(snippet), 400)]

                recommendedProblems.append({'spojId':problem, 'url':url, 'title':title, 'snippet':snippet})
                cnt += 1
		    
            return recommendedProblems
		    
    return []

if __name__ == "__main__":
    create_default_recommender()
    #print rec("ederfmartins", 10)
