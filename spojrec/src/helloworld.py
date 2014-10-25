from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

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
        
        #result = DonloadQueueRecord.query().fetch(5000)
        #self.response.write('<pre>len(DonloadQueueRecord)='+ str(len(result)) +'</pre>')
        #for data in result:
        #    data.key.delete()
        
        result = ProblemItem.query().fetch(1000)
        self.response.write('<pre>len(ProblemItem)='+ str(len(result)) +'</pre>')
        
        result = UserItem.query().fetch(20000)
        self.response.write('<pre>len(UserItem)='+ str(len(result)) +'</pre>')
        
        result = SubmissionsItem.query().fetch(20000)
        self.response.write('<pre>len(SubmissionsItem)='+ str(len(result)) +'</pre>')
        
            


application = webapp.WSGIApplication([('/helloworld', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
