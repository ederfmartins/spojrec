from google.appengine.ext import ndb

class UserItem(ndb.Model):
    """Store data about users of spoj"""
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty()
    country = ndb.StringProperty()
    school = ndb.StringProperty()
    url = ndb.StringProperty()
    
class SubmissionsItem(ndb.Model):
    """Store data about problems submited to spoj"""
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    data = ndb.TextProperty()
    url = ndb.StringProperty()
        
class ProblemItem(ndb.Model):
    """Store data about problems of spoj"""
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    url = ndb.StringProperty()
    snippet = ndb.TextProperty()


def update_problem(identifier, title, url, snippet):
    key = ndb.Key(ProblemItem, identifier)
    p = ProblemItem(key=key, title=title, url=url, snippet=snippet)
    p.put()

def update_user(identifier, name, url, country, school):
    key = ndb.Key(UserItem, identifier)
    p = UserItem(key=key, name=name, url=url, country=country, school=school)
    p.put()

def update_user_submissions(identifier, data, url):
    key = ndb.Key(SubmissionsItem, identifier)
    p = SubmissionsItem(key=key, data=data, url=url)
    p.put()
