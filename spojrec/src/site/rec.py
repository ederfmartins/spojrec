from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Attr:
    def __init__(self, attr, value):
        self.attr = attr
        self.value = value
    
    def __repr__(self):
        return self.attr + '="' + self.value + '"'

class HtmlElement:
    def __init__(self, tagName):
        self.tagName = tagName
        self.attrs = []
        self.childrem = []
    
    def addAttr(self, attr):
        self.attrs.append(attr)
        return self
    
    def addNode(self, node):
        self.childrem.append(node)
        return node
        
    def __repr__(self):
        start = '<' + self.tagName
        
        for attr in self.attrs:
            start += ' ' + str(attr) 
        
        start += '>'
        end = '</' + self.tagName + '>'
        body = ''.join(str(x) for x in self.childrem)
        return start + body + end

class RecPage(webapp.RequestHandler):
    
    def __init__(self, request, response):
        super(webapp.RequestHandler, self).__init__()
        self.initialize(request, response)
        self.resultTable = []
        
    def get_head(self):
        head = HtmlElement('head')
        
        meta = HtmlElement('meta')
        meta.addAttr(Attr('http-equiv', 'Content-type'))
        meta.addAttr(Attr('content', 'text/html; charset=utf-8'))
        head.addNode(meta)
        
        css = HtmlElement('link')
        css.addAttr(Attr('rel', 'stylesheet'))
        css.addAttr(Attr('type', 'text/css'))
        css.addAttr(Attr('href', 'style.css'))
        head.addNode(css)
        
        title = HtmlElement('title')
        title.addNode('Spojrec')
        head.addNode(title)
        
        return head
    
    def body(self):
        form = HtmlElement('form')
        form.addAttr(Attr('action', "/"))
        form.addAttr(Attr('method', "post"))
        form.addAttr(Attr('name', "form1"))
        
        div = HtmlElement('div')
        div.addAttr(Attr('class', "maindiv"))
        div.addAttr(Attr('align', "center"))
        form.addNode(div)
        
        logoDiv = HtmlElement('div')
        logoDiv.addNode(HtmlElement('img').addAttr(Attr('src', 'logo.png')))
        logoDiv.addAttr(Attr('class', "top"))
        div.addNode(logoDiv)
        
        searchDiv = HtmlElement('div')
        searchDiv.addAttr(Attr('class', "inner"))
        div.addNode(searchDiv)
        
        query = HtmlElement('input')
        query.addAttr(Attr('id', 'userId'))
        query.addAttr(Attr('name', 'userId'))
        query.addAttr(Attr('placeholder', "Your spoj's user name"))
        query.addAttr(Attr('class', "searchInput"))
        searchDiv.addNode(query)
        
        search = HtmlElement('input')
        search.addAttr(Attr('type', "submit"))
        search.addAttr(Attr('value', "Search"))
        search.addAttr(Attr('class', "searchButton"))
        searchDiv.addNode(search)
        
        if len(self.resultTable) > 0:
            resultDiv = HtmlElement('div')
            resultDiv.addAttr(Attr('class', 'resultDiv'))
            for result in self.resultTable:
                resultDiv.addNode(result)
            div.addNode(resultDiv)
        
        body = HtmlElement('body')
        body.addAttr(Attr('style', 'background-image:url(balloon-release.jpg);background-size: cover;'))
        body.addNode(form)
        return body
    
    def get_html(self):
        return '<html>' + str(self.get_head()) + str(self.body()) + '</html>'
        
    
    def post(self):
        spojId = self.request.get("userId")
        self.resultTable.append(spojId)
        self.get()
        
    
    def get(self):
        self.response.write(self.get_html())

application = webapp.WSGIApplication([('/', RecPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()