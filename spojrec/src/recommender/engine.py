from google.appengine.api import memcache
from basicdefs import DEFAULT_RECOMMENDER

def _is_valid_problem(spojId):
    return True

def _is_valid_user(spojId):
    return False

def rec(spojId, topk=5):
    if _is_valid_problem(spojId):
        recommendedProblems = []
        #recommendedProblems.append({'spojId':'teste1', 'url':'www.xxxxx', 'title':'bal ldj a aaa'})
        #recommendedProblems.append({'spojId':'teste2', 'url':'br.spoj.xx', 'title':'Mais um teste'})
        memcacheClient = memcache.Client()
        rec = memcacheClient.gets(DEFAULT_RECOMMENDER)
        
        recProblems = rec.rec(spojId, topk)
        cnt = 0
        for (problem, score) in recProblems:
            if cnt >= topk:
                break
            
            recommendedProblems.append({'spojId':problem, 'url':'http://br.spoj.com/' + problem, 'title':'bal ldj a aaa'})
    
            cnt += 1
        
        return recommendedProblems
    elif _is_valid_user(spojId):
        pass