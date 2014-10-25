from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

class TestRec(webapp.RequestHandler):
    def get(self):
        self.memcacheClient = memcache.Client()
        
        test = self.memcacheClient.gets('testrec')
        
        self.response.write('meu teste foi = ' + test)

application = webapp.WSGIApplication([('/testrec', TestRec)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()