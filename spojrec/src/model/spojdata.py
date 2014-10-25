from google.appengine.ext import ndb    

class UserItem(ndb.Model):
    """Store data about users of spoj"""
    spojId = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty()
    country = ndb.StringProperty()
    school = ndb.StringProperty()
    url = ndb.StringProperty()
    
class SubmissionsItem(ndb.Model):
    """Store data about problems submited to spoj"""
    spojId = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    data = ndb.TextProperty()
    url = ndb.StringProperty()
        
class ProblemItem(ndb.Model):
    """Store data about problems of spoj"""
    spojId = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    url = ndb.StringProperty()
    snippet = ndb.TextProperty()
    