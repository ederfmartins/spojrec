import re
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from downloadQueue import DonloadQueue

START_SEED = 'http://br.spoj.com'
START_SEED_PATTERN = 'br\.spoj\.com'

def allow_spoj_domain(url):
    logging.debug('allow_spoj_domain(' + url + ')')
    domainPattern = re.compile(START_SEED_PATTERN)
    return domainPattern.search(url)

class CrawnSpoj(webapp.RequestHandler):
    
    def post(self):
        self.get()
    
    def get(self):
        myqueue = DonloadQueue()
        myqueue.add_follow_func(allow_spoj_domain)
        myqueue.restart([START_SEED])
    

application = webapp.WSGIApplication([('/crawnspojstart', CrawnSpoj)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()