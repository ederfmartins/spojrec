import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.api import background_thread

from recommender.rec import Dacu, get_acepted_problems
from recommender.database import ProblemsDatabase
from recommender.metrics import Metrics

from basicdefs import DEFAULT_RECOMMENDER

def create_default_recommender(arg1, arg2, *kwargs):
    database = ProblemsDatabase()
    metrics = Metrics(database.get_test())
    test = get_acepted_problems(database.get_problems_by_user())
    
    dacu = Dacu(metrics, test)
    
    memcacheClient = memcache.Client()
    memcacheClient.add(key=DEFAULT_RECOMMENDER, value=dacu, time=24*3600)

class ComputeMetrics(webapp.RequestHandler):
    def get(self):
        logging.debug('Starting re computation of metrics needed in recommendation process.')
        background_thread.start_new_background_thread(create_default_recommender)
        self.response.write('ok')

application = webapp.WSGIApplication([('/_ah/start', ComputeMetrics), ('/compmetrics', ComputeMetrics)], debug=True)


def main():
    logging.info('->Starting re computation of metrics needed in recommendation process.')
    run_wsgi_app(application)
    memcacheClient = memcache.Client()
    rec = memcacheClient.gets(DEFAULT_RECOMMENDER)
    if rec is None:
        background_thread.start_new_background_thread(create_default_recommender)

if __name__ == "__main__":
    main()