#!/usr/bin/python

import os
import webapp2 as webapp
from constants import VIRTUAL_ENV_DIR, HTTP_PORT, HTTP_HOST, PRODUCTION
from constants import USER_NAME

try:
    virtenv = VIRTUAL_ENV_DIR + '/virtenv/'
    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
    execfile(virtualenv, dict(__file__=virtualenv))
#except IOError:
except:
    pass

from webpages.mainpage import RecPage
from webpages.statistics import UserStatisticsPage

application = webapp.WSGIApplication([('/', RecPage), 
                                      ('/users/(.+)/(' + USER_NAME + ')', UserStatisticsPage)], debug=not PRODUCTION)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    import webapp2 as webapp
    from paste.urlparser import StaticURLParser
    from paste.cascade import Cascade
    
    static_app = StaticURLParser("wsgi/")
    app = Cascade([static_app, application])
    
    httpd = make_server(HTTP_HOST, HTTP_PORT, app)
    httpd.serve_forever()

