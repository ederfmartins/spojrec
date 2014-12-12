# -*- coding: utf-8 -*-

import sys
import random

import webapp2 as webapp

from webpages.html import Attr, HtmlElement
from recommender.engine import rec
from constants import SPOJ_URLS

class RecPage(webapp.RequestHandler):
    
    def __init__(self, request, response):
        super(webapp.RequestHandler, self).__init__()
        self.initialize(request, response)
        self.searchInputId = 'spojId'
        self.difId = 'dif'
        self.spojDB = 'contest'
        self.dificulties = ['Normal', 'Facil', 'Dificil']
        self.contests = SPOJ_URLS
        
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
        
    def get_query_button(self, spojId):
        query = HtmlElement('input')
        query.addAttr(Attr('id', self.searchInputId))
        query.addAttr(Attr('name', self.searchInputId))
        if spojId != '':
            query.addAttr(Attr('value', spojId))
        query.addAttr(Attr('placeholder', "id de um usuário ou problema do spoj"))
        query.addAttr(Attr('class', "searchInput"))
        return query
        
    def get_search_button(self):
        search = HtmlElement('input')
        search.addAttr(Attr('type', "submit"))
        search.addAttr(Attr('value', "Buscar"))
        search.addAttr(Attr('class', "searchButton"))
        return search
    
    def get_prob_dificult_combo(self, selected):
        combo = HtmlElement('select')
        combo.addAttr(Attr('name', self.difId))
        combo.addAttr(Attr('id', self.difId))
        combo.addAttr(Attr('value', selected))
        for dificult in self.dificulties:
        	item = HtmlElement('option')
        	item.addAttr(Attr('value', dificult))
        	if dificult == selected:
        	    item.addAttr(Attr('SELECTED', ''))
        	item.addNode(dificult)
        	combo.addNode(item)
        
        span = HtmlElement('span').addNode('Dificuldade dos problemas:')
        div = HtmlElement('div').addAttr(Attr('class', 'difdiv'))
        div.addNode(span)
        div.addNode(combo)
        return div
    
    def get_db_combo(self, db):
        span = HtmlElement('span').addNode('SPOJ contest:')
        div = HtmlElement('div').addAttr(Attr('class', 'contestDiv'))
        div.addNode(span)
        for contest in self.contests:
            radio = HtmlElement('input')
            radio.addAttr(Attr('type', 'radio'))
            radio.addAttr(Attr('name', self.spojDB))
            radio.addAttr(Attr('id', contest))
            radio.addAttr(Attr('value', contest))
            
            if contest == db:
                radio.addAttr(Attr('checked', ''))
            
            div.addNode(radio)
            div.addNode(contest)
            
        return div
    
    def add_logo_div(self, mainDiv, cssClass):
        logoDiv = HtmlElement('div')
        logoDiv.addNode(HtmlElement('img').addAttr(Attr('src', 'static/logo.png')))
        logoDiv.addAttr(Attr('class', cssClass))
        mainDiv.addNode(logoDiv)
    
    def add_search_div(self, mainDiv, cssclass, spojId, selected, db):
        searchDiv = HtmlElement('div')
        searchDiv.addAttr(Attr('class', cssclass))
        mainDiv.addNode(searchDiv)
        
        searchDiv.addNode(self.get_query_button(spojId))
        searchDiv.addNode(self.get_search_button())
        searchDiv.addNode(self.get_prob_dificult_combo(selected))
        searchDiv.addNode(self.get_db_combo(db))
        
    def get(self):
        form = self.create_form()
        mainDiv = self.create_mainDiv(form)
        self.add_logo_div(mainDiv, 'top')
        
        mainDiv.addNode(self.create_aboutDiv())
        mainDiv.addNode(self.create_aboutText())
        
        self.add_search_div(mainDiv, 'inner', '', 'Normal', 'BR')
        
        body = HtmlElement('body')
        body.addAttr(Attr('style', 'background-image:url(static/balloon-release.jpg);background-size: cover;'))
        body.addNode(form)
        
        self.response.write('<html>' + str(self.get_head()) + str(body) + '</html>')
        
    
    def post(self):
        spojId = self.request.get(self.searchInputId)
        dificult = self.request.get(self.difId)
        database = self.request.get(self.spojDB)
        recommendedProblems = rec(spojId, database, dificult)
        
        form = self.create_form()
        mainDiv = self.create_mainDiv(form)
        
        self.add_logo_div(mainDiv, 'top1')
        
        mainDiv.addNode(self.create_aboutDiv())
        mainDiv.addNode(self.create_aboutText())
        
        self.add_search_div(mainDiv, 'innerPost', spojId, dificult, database)
        
        if len(recommendedProblems) > 0:
            resultDiv = HtmlElement('div')
            resultDiv.addAttr(Attr('class', 'resultDiv'))
            
            linkToUser = HtmlElement('a').addAttr(Attr('href', '/users/' + database + '/' + spojId))
            linkToUser.addAttr(Attr('style', 'color:red;'))
            linkToUser.addNode(spojId)
            
            tableTop = HtmlElement('h3').addAttr(Attr('class', 'text-warning'))
            tableTop.addNode('Porque recomendamos esses problemas para ' + str(linkToUser))
            resultDiv.addNode(tableTop)
            
            for problem in recommendedProblems:
                problemH3 = HtmlElement('h3')
                
                if isinstance(problem['title'], unicode):
                    problem['title'] = problem['title'].encode('utf-8','ignore')
                
                if isinstance(problem['snippet'], unicode):
                    problem['snippet'] = problem['snippet'].encode('utf-8','ignore')
                
                l = HtmlElement('a').addAttr(Attr('href', problem['url'])).addNode(str(problem['spojId']) + ' - ' + str(problem['title']))
                problemH3.addNode(HtmlElement('img').addAttr(Attr('src', 'static/ballon' + str(random.randint(1,7)) + '.png')))
                problemH3.addNode(l)
                resultDiv.addNode(problemH3)
                resultDiv.addNode(HtmlElement('p').addNode(problem['snippet']))
                
            mainDiv.addNode(resultDiv)
        
        body = HtmlElement('body')
        body.addAttr(Attr('style', 'background-image:url(static/balloon-release.jpg);background-size: cover;'))
        body.addNode(form)
        
        self.response.write('<html>' + str(self.get_head()) + str(body) + '</html>')


