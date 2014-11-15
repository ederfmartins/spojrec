import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import ndb

#from lxml.html import parse
#from urllib2 import urlopen

from model.spojdata import ProblemItem, SubmissionsItem, UserItem

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('Hello, webapp World!')
        self.crawnSpoj()
    
    def crawnSpoj(self):
        #url = 'http://br.spoj.com'
        #page = urlopen(url)
        #doc = parse(page).getroot()
        #doc.make_links_absolute(url)
        
        #for link in doc.iterlinks():
        #    self.response.write(link)
        #    self.response.write('<br>')
            
        self.response.write('<pre>testeeeee!!!!</pre>')
        
        #teste = TestKind(key_name='um teste', spojId='teste', title='sera que isso vai funcionar?')
        #teste.put()
        
        #TestKind1(key=ndb.Key(TestKind1, 'eder'), spojId='teste', title='sera que isso vai funcionar?').put()
        
        #key = ndb.Key(TestKind1, 'Sandy')
        #entidade = key.get()
        #entidade.spojId ='teste'
        #entidade.title ='sera que isso vai funcionar?'
        #entidade.timestamp = datetime.datetime.now()
        #entidade.put()
        
            


application = webapp.WSGIApplication([('/helloworld', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
