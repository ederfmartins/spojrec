# -*- coding: utf-8 -*-

import sys
import webapp2 as webapp

from constants import SPOJ_URLS
from webpages.html import Attr, HtmlElement
from datamodel.database import Database
from crawler.dataExtractor.signedlistParser import parseSignedlist
from recommender.util import sumarise_problems_by_column, sumarize_stats_of_user, sumarize_submissions_by_month


class UserStatisticsPage(webapp.RequestHandler):
    
    def __init__(self, request, response):
        super(webapp.RequestHandler, self).__init__()
        self.initialize(request, response)
    
    
    def get_head(self):
        head = HtmlElement('head')
        
        meta = HtmlElement('meta')
        meta.addAttr(Attr('http-equiv', 'Content-type'))
        meta.addAttr(Attr('content', 'text/html; charset=utf-8'))
        head.addNode(meta)
        
        links = ['/static/style.css', '//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css']
        for link in links:
		    css = HtmlElement('link')
		    css.addAttr(Attr('rel', 'stylesheet'))
		    css.addAttr(Attr('type', 'text/css'))
		    css.addAttr(Attr('href', link))
		    head.addNode(css)
        
        scripts = ['/static/script.js', '//code.jquery.com/jquery-1.10.2.js', '//code.jquery.com/ui/1.11.2/jquery-ui.js']
        for script in scripts:
		    js = HtmlElement('script')
		    js.addAttr(Attr('src', script))
		    head.addNode(js)
        
        title = HtmlElement('title')
        title.addNode('Spojrec')
        head.addNode(title)
        
        return head
    
    
    def build_user_info_div(self, database, userId, body):
        user = database.find_user(userId)
        body.addNode(HtmlElement('h3').addNode('Usuário: ' + user['name'].encode('utf-8','ignore')))
        body.addNode(HtmlElement('h3').addNode('País: ' + user['country'].encode('utf-8','ignore')))
        body.addNode(HtmlElement('h3').addNode('Instituição: ' + user['school'].encode('utf-8','ignore')))
        body.addNode(HtmlElement('h3').addNode('Pontuação atual: -'))
        body.addNode(HtmlElement('h3').addNode('Ranking atual: -'))
        body.addNode(HtmlElement('h3').addNode('Tópicos mais tentados: -'))
    
    
    def build_stats_div(self, database, userId, head, body):
        allProblems = parseSignedlist(database.get_problems_of_user_from_db(userId)['data'])
        
        problems = sumarise_problems_by_column(allProblems, 'RESULT')
        subTable = self.build_submission_stats_table(problems)
        probTable = self.build_problems_stats_table(allProblems)
        table = HtmlElement('table')
        table.addAttr(Attr('class', 'allStats'))
        body.addNode(table)
        tr = HtmlElement('tr')
        table.addNode(tr)
        tr.addNode(HtmlElement('td').addNode(probTable))
        tr.addNode(HtmlElement('td').addNode(subTable))
        
        self.build_submitions_chart(allProblems, head, body)
    
    
    
    def build_submitions_chart(self, allProblems, head, body):
        points = sumarize_submissions_by_month(allProblems)
        dataPoints = ''
        
        for point in sorted(points):
            dataPoints += ', ["' + point + '",' + str(points[point]) + ']'
        
        script = HtmlElement('script')
        script.addAttr(Attr('type', 'text/javascript'))
        script.addAttr(Attr('src', 'https://www.google.com/jsapi'))
        head.addNode(script)
        
        drawChart = HtmlElement('script')
        drawChart.addAttr(Attr('type', 'text/javascript'))
        head.addNode(drawChart)
        drawChart.addNode("""
        google.load("visualization", "1", {packages:["corechart"]});
        google.setOnLoadCallback(drawChart);
        
        function drawChart() 
        {
            var data = google.visualization.arrayToDataTable([ ['Data', '# tentativas']""" + dataPoints + """]);
            var options = { title: 'Histórico de submissão de problemas', };
            var chart = new google.visualization.AreaChart(document.getElementById('submitions_chart'));
            chart.draw(data, options);
        }
        """)
        
        chartDiv = HtmlElement('div')
        chartDiv.addAttr(Attr('class', 'chartDiv'))
        chartDiv.addNode(HtmlElement('div').addAttr(Attr('id', 'submitions_chart')))
        body.addNode(chartDiv)
    
    
        
    def build_submission_stats_table(self, problems):
        subTable = HtmlElement('table')
        subTable.addAttr(Attr('class', 'statTable'))
        th = HtmlElement('tr').addNode(HtmlElement('th').addAttr(Attr('colspan', '2')).addNode('Submissões'))
        subTable.addNode(th)
        
        totalTr = HtmlElement('tr')
        subTable.addNode(totalTr)
        total = 0
        
        for result in sorted(problems):
            n = len(problems[result])
            total += n
            tr = HtmlElement('tr')
            subTable.addNode(tr)
            tr.addNode(HtmlElement('td').addNode(result))
            tr.addNode(HtmlElement('td').addNode(n))
        
        
        totalTr.addNode(HtmlElement('td').addNode('Total'))
        totalTr.addNode(HtmlElement('td').addNode(total))
        return subTable
    
    
    def build_problems_stats_table(self, problems):
        problems = sumarise_problems_by_column(problems, 'PROBLEM')
        stats = sumarize_stats_of_user(problems)
        
        probTable = HtmlElement('table')
        probTable.addAttr(Attr('class', 'statTable'))
        th = HtmlElement('tr').addNode(HtmlElement('th').addAttr(Attr('colspan', '2')).addNode('Problemas'))
        probTable.addNode(th)
        
        labels = ['Problemas tentados', 'Resolvidos', 'Não resolvidos', 'Resolvidos na 1ª tentativa', 'Mais tentados', 'Média de tentativas']
        values = [stats['attempted'], stats['solved'], stats['failures'], stats['accepted_1'], stats['most_failures'], '%.2f' % stats['avg_attempted_per_problem']]
        cnt = 0
        
        for label in labels:
            tr = HtmlElement('tr')
            tr.addNode(HtmlElement('td').addNode(label))
            tr.addNode(HtmlElement('td').addNode(values[cnt]))
            cnt += 1
            probTable.addNode(tr)
            
        return probTable
        
            
    def build_probs_table(self, problems, contest):
        table = HtmlElement('table')
        table.addAttr(Attr('style', 'width: 95%;padding: 4px 4px 4px 4px;'))
        
        cnt = 0
        tr = None

        for p in problems:
            if cnt % 10 == 0: #10 colunas
                tr = HtmlElement('tr')
                table.addNode(tr)
                
            td = HtmlElement('td')
            td.addNode(HtmlElement('a').addAttr(Attr('href', SPOJ_URLS[contest] + '/problems/' + p)).addNode(p))
            tr.addNode(td)
            cnt += 1
        
        return table
    
        
    def build_solve_prob_div(self, database, userId, contest, body):
        title = HtmlElement('h2').addAttr(Attr('class', 'center-align')).addNode('Problemas resolvidos pelo usuário')
        body.addNode(title)
        
        allProblems = parseSignedlist(database.get_problems_of_user_from_db(userId)['data'])
        problems = sumarise_problems_by_column(allProblems, 'PROBLEM')
        body.addNode(self.build_probs_table(problems, contest))
        
    
    def get(self, contest, userId):
        database = Database(contest)
        uNameH1 = HtmlElement('h1').addAttr(Attr('class', 'center-align'))
        uNameH1.addNode(userId)
        
        contestH2 = HtmlElement('h2').addAttr(Attr('class', 'center-align'))
        contestH2.addNode(HtmlElement('a').addAttr(Attr('href', SPOJ_URLS[contest])).addNode('SPOJ ' + contest))
        
        head = self.get_head()
        body = HtmlElement('body').addAttr(Attr('style', 'background-color:gray;'))
        body.addNode(uNameH1)
        body.addNode(contestH2)
        self.build_user_info_div(database, userId, body)
        self.build_stats_div(database, userId, head, body)
        self.build_solve_prob_div(database, userId, contest, body)
        self.response.write('<html>' + str(head) + str(body) + '</html>')
