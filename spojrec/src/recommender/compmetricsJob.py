from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

class ComputeMetrics(webapp.RequestHandler):
    def get(self):
        self.memcacheClient = memcache.Client()
        self.memcacheClient.add(key='testrec', value='Algum comentário ridiculamente trivial.', time=5*3600)

application = webapp.WSGIApplication([('/compmetricsstart', ComputeMetrics)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()