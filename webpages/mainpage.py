# -*- coding: utf-8 -*-
import webapp2 as webapp

from webpages.html import Attr, HtmlElement
from recommender.engine import rec

class RecPage(webapp.RequestHandler):
    
    def __init__(self, request, response):
        super(webapp.RequestHandler, self).__init__()
        self.initialize(request, response)
        
    def get_head(self):
        head = HtmlElement('head')
        
        meta = HtmlElement('meta')
        meta.addAttr(Attr('http-equiv', 'Content-type'))
        meta.addAttr(Attr('content', 'text/html; charset=utf-8'))
        head.addNode(meta)
        
        links = ['static/style.css', '//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css']
        for link in links:
		    css = HtmlElement('link')
		    css.addAttr(Attr('rel', 'stylesheet'))
		    css.addAttr(Attr('type', 'text/css'))
		    css.addAttr(Attr('href', link))
		    head.addNode(css)
        
        scripts = ['static/script.js', '//code.jquery.com/jquery-1.10.2.js', '//code.jquery.com/ui/1.11.2/jquery-ui.js']
        for script in scripts:
		    js = HtmlElement('script')
		    js.addAttr(Attr('src', script))
		    head.addNode(js)
        
        dilogScript = HtmlElement('script')
        dilogScript.addNode('''$(function() {
    $( "#dialog" ).dialog({
      autoOpen: false,
      show: {
        effect: "blind",
        duration: 100
      },
      hide: {
        effect: "blind",
        duration: 100
      }
    });
 
    $( "#opener" ).click(function() {
      $( "#dialog" ).dialog( "open" );
    });
  });''')
        head.addNode(dilogScript)
        
        title = HtmlElement('title')
        title.addNode('Spojrec')
        head.addNode(title)
        
        return head
    
    
    def create_form(self):
        form = HtmlElement('form')
        form.addAttr(Attr('action', "/"))
        form.addAttr(Attr('method', "post"))
        form.addAttr(Attr('name', "form1"))
        return form
    
    def create_mainDiv(self, form):    
        div = HtmlElement('div')
        div.addAttr(Attr('class', "maindiv"))
        div.addAttr(Attr('align', "center"))
        form.addNode(div)
        
        return div   
        
    def create_aboutDiv(self):
        aboutDiv = HtmlElement('div')
        aboutDiv.addNode(HtmlElement('img').addAttr(Attr('src', 'static/about.jpg')).addAttr(Attr('id', 'opener')).addAttr(Attr('title', 'Sobre o site')))
        aboutDiv.addAttr(Attr('class', "abouttop"))
        return aboutDiv
        
    def create_aboutText(self):
        aboutDiv = HtmlElement('div')
        aboutDiv.addNode('<p>Spojrec é uma aplicação web, que tem como intuito fornecer recomendações de problemas para o spoj.</p>')
        aboutDiv.addAttr(Attr('id', "dialog"))
        aboutDiv.addAttr(Attr('title', "Sobre"))
        return aboutDiv
        
    def get_query_button(self):
        query = HtmlElement('input')
        query.addAttr(Attr('id', 'userId'))
        query.addAttr(Attr('name', 'userId'))
        query.addAttr(Attr('placeholder', "id de um usuário ou problema do spoj"))
        query.addAttr(Attr('class', "searchInput"))
        return query
        
    def get_search_button(self):
        search = HtmlElement('input')
        search.addAttr(Attr('type', "submit"))
        search.addAttr(Attr('value', "Buscar"))
        search.addAttr(Attr('class', "searchButton"))
        return search
    
    def add_logo_div(self, mainDiv, cssClass):
        logoDiv = HtmlElement('div')
        logoDiv.addNode(HtmlElement('img').addAttr(Attr('src', 'static/logo.png')))
        logoDiv.addAttr(Attr('class', cssClass))
        mainDiv.addNode(logoDiv)
        
    def get(self):
        form = self.create_form()
        mainDiv = self.create_mainDiv(form)
        self.add_logo_div(mainDiv, 'top')
        
        mainDiv.addNode(self.create_aboutDiv())
        mainDiv.addNode(self.create_aboutText())
        
        searchDiv = HtmlElement('div')
        searchDiv.addAttr(Attr('class', "inner"))
        mainDiv.addNode(searchDiv)
        
        searchDiv.addNode(self.get_query_button())
        searchDiv.addNode(self.get_search_button())
        
        body = HtmlElement('body')
        body.addAttr(Attr('style', 'background-image:url(static/balloon-release.jpg);background-size: cover;'))
        body.addNode(form)
        
        self.response.write('<html>' + str(self.get_head()) + str(body) + '</html>')
        
    
    def post(self):
        spojId = self.request.get("userId")
        recommendedProblems = rec(spojId)
        
        form = self.create_form()
        mainDiv = self.create_mainDiv(form)
        
        self.add_logo_div(mainDiv, 'top1')
        
        mainDiv.addNode(self.create_aboutDiv())
        mainDiv.addNode(self.create_aboutText())
        
        searchDiv = HtmlElement('div')
        searchDiv.addAttr(Attr('class', "innerPost"))
        mainDiv.addNode(searchDiv)
        
        searchDiv.addNode(self.get_query_button())
        searchDiv.addNode(self.get_search_button())
        
        if len(recommendedProblems) > 0:
            resultDiv = HtmlElement('div')
            resultDiv.addAttr(Attr('class', 'resultDiv'))
            
            tableTop = HtmlElement('h3').addAttr(Attr('class', 'text-warning'))
            tableTop.addNode('Problemas recomendados para ' + spojId)
            resultDiv.addNode(tableTop)
            
            #cnt = 1
            #resultTable = HtmlElement('table').addAttr(Attr('class', 'recProbTable'))
            
            #th = HtmlElement('tr')
            #th.addNode(HtmlElement('th').addNode('#'))
            #th.addNode(HtmlElement('th').addNode('Problemas recomendados para ' + self.spojId))
            #th.addNode(HtmlElement('th').addNode('Problemas Fáceis'))
            #resultTable.addNode(th)
            
            for problem in recommendedProblems:
                #tr = HtmlElement('tr')
                #tr.addNode(HtmlElement('td').addNode(str(cnt)))
                ##tr.addNode(HtmlElement('td').addNode(HtmlElement('a').addAttr(Attr('href', problem['url'])).addNode(problem['title'])))
                #tr.addNode(HtmlElement('td').addNode(HtmlElement('a').addAttr(Attr('href', problem['url'])).addNode(problem['spojId'])))
                #resultTable.addNode(tr)
                problemH3 = HtmlElement('h3')
                l = HtmlElement('a').addAttr(Attr('href', problem['url'])).addNode(problem['spojId'] + ' - ' + problem['title'])
                problemH3.addNode(l)
                resultDiv.addNode(problemH3)
                resultDiv.addNode(HtmlElement('p').addNode(problem['snippet']))
                #cnt += 1
            
            #resultDiv.addNode(resultTable)
            mainDiv.addNode(resultDiv)
        
        body = HtmlElement('body')
        body.addAttr(Attr('style', 'background-image:url(static/balloon-release.jpg);background-size: cover;'))
        body.addNode(form)
        
        self.response.write('<html>' + str(self.get_head()) + str(body) + '</html>')
        

application = webapp.WSGIApplication([('/', RecPage)], debug=True)

