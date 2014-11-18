# -*- coding: utf-8 -*-

try:
    import webapp2 as webapp
except ImportError:
	from google.appengine.ext import webapp
	from google.appengine.ext.webapp.util import run_wsgi_app

try:
    from spojrec.src.webpages.html import Attr, HtmlElement
    from spojrec.src.recommender.engine import rec
except ImportError:
    from webpages.html import Attr, HtmlElement
    from recommender.engine import rec

class RecPage(webapp.RequestHandler):
    
    def __init__(self, request, response):
        super(webapp.RequestHandler, self).__init__()
        self.initialize(request, response)
        self.recommendedProblems = []
        self.spojId = ''
        
    def get_head(self):
        head = HtmlElement('head')
        
        meta = HtmlElement('meta')
        meta.addAttr(Attr('http-equiv', 'Content-type'))
        meta.addAttr(Attr('content', 'text/html; charset=utf-8'))
        head.addNode(meta)
        
        css = HtmlElement('link')
        css.addAttr(Attr('rel', 'stylesheet'))
        css.addAttr(Attr('type', 'text/css'))
        css.addAttr(Attr('href', 'static/style.css'))
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
        logoDiv.addNode(HtmlElement('img').addAttr(Attr('src', 'static/logo.png')))
        logoDiv.addAttr(Attr('class', "top"))
        div.addNode(logoDiv)
        
        searchDiv = HtmlElement('div')
        searchDiv.addAttr(Attr('class', "inner"))
        div.addNode(searchDiv)
        
        query = HtmlElement('input')
        query.addAttr(Attr('id', 'userId'))
        query.addAttr(Attr('name', 'userId'))
        query.addAttr(Attr('placeholder', "id de um usuário ou problema do spoj"))
        query.addAttr(Attr('class', "searchInput"))
        searchDiv.addNode(query)
        
        search = HtmlElement('input')
        search.addAttr(Attr('type', "submit"))
        search.addAttr(Attr('value', "Buscar"))
        search.addAttr(Attr('class', "searchButton"))
        searchDiv.addNode(search)
        
        if len(self.recommendedProblems) > 0:
            resultDiv = HtmlElement('div')
            resultDiv.addAttr(Attr('class', 'resultDiv'))
            
            tableTop = HtmlElement('h3').addAttr(Attr('class', 'text-warning center-align'))
            tableTop.addNode('Problemas recomendados para ' + self.spojId)
            resultDiv.addNode(tableTop)
            
            cnt = 1
            resultTable = HtmlElement('table').addAttr(Attr('class', 'recProbTable'))
            
            th = HtmlElement('tr')
            th.addNode(HtmlElement('th').addNode('#'))
            #th.addNode(HtmlElement('th').addNode('Problemas recomendados para ' + self.spojId))
            th.addNode(HtmlElement('th').addNode('Problemas Fáceis'))
            th.addNode(HtmlElement('th').addNode('Problemas Difíceis'))
            resultTable.addNode(th)
            
            for problem in self.recommendedProblems:
                tr = HtmlElement('tr')
                tr.addNode(HtmlElement('td').addNode(str(cnt)))
                #tr.addNode(HtmlElement('td').addNode(HtmlElement('a').addAttr(Attr('href', problem['url'])).addNode(problem['title'])))
                tr.addNode(HtmlElement('td').addNode(HtmlElement('a').addAttr(Attr('href', problem['url'])).addNode(problem['spojId'])))
                tr.addNode(HtmlElement('td').addNode(HtmlElement('a').addAttr(Attr('href', problem['url'])).addNode(problem['spojId'])))
                resultTable.addNode(tr)
                cnt += 1
            
            resultDiv.addNode(resultTable)
            div.addNode(resultDiv)
        
        body = HtmlElement('body')
        body.addAttr(Attr('style', 'background-image:url(static/balloon-release.jpg);background-size: cover;'))
        body.addNode(form)
        return body
    
    def get_html(self):
        return '<html>' + str(self.get_head()) + str(self.body()) + '</html>'
        
    
    def post(self):
        self.spojId = self.request.get("userId")
        self.recommendedProblems = rec(self.spojId)
        self.get()
        
    
    def get(self):
        self.response.write(self.get_html())

application = webapp.WSGIApplication([('/', RecPage)], debug=True)


#def main():
#    run_wsgi_app(application)

#if __name__ == "__main__":
#    main()

