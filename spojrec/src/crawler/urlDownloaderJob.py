# -*- coding: utf-8 -*-

import re
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from lxml.html import tostring

from downloadQueue import DonloadQueue
from basicdefs import PROBLEM_NAME
from basicdefs import PROBLENS_PAGE_PATTERN, USERS_PAGE_PATTERN, SUBMISSIONS_PAGE_PATTERN
from basicdefs import WORKER_QUEUE_URL
from model.spojdata import update_problem, update_user, update_user_submissions

START_SEED = 'http://br.spoj.com'

#links
PROBLEMS_LIST_PATTERN = '.*/problems/[a-z0-9_]+/$'
PROBLEMS_LIST1_PATTERN = '.*/problems/[a-z0-9_]+/sort=0,start=\d+'
PROBLENS_LIST2_PATTERN = '.*/problems/' + PROBLEM_NAME + '/cstart=\d+$'
RANKS_PAGE_PATTERN = '.*/ranks/.*'
RANKS_PAGE_PATTERN_EXCLUDE = '.*/ranks/' + PROBLEM_NAME + '/.*lang=.*'
PROBLENS_PAGE_PATTERN_INCLUDE ='.*/problems/' + PROBLEM_NAME + '/.*cstart=.*'

LINKS_ALLOWED = [re.compile(PROBLENS_PAGE_PATTERN),
                 re.compile(USERS_PAGE_PATTERN),
                 re.compile(SUBMISSIONS_PAGE_PATTERN),
                 re.compile(PROBLENS_PAGE_PATTERN_INCLUDE), 
                 re.compile(RANKS_PAGE_PATTERN),
                 re.compile(PROBLEMS_LIST_PATTERN),
                 re.compile(PROBLEMS_LIST1_PATTERN),
                 re.compile(PROBLENS_LIST2_PATTERN)]

LINKS_DENIED = re.compile(RANKS_PAGE_PATTERN_EXCLUDE)

def extract_unique_element(xpath):
    assert len(xpath) <= 1
    if len(xpath) == 1:
        return xpath[0]
    else:
        return ''


def parse_problem(doc, url):
    spojId = url.split('/problems/')[1].split('/.+')[0].replace('/', '')
    title = extract_unique_element(doc.xpath('//div[@class="prob"]/table/tr/td/h1/text()'))
    snippet = extract_unique_element(doc.xpath('//h3[text()="Tarefa"]/preceding-sibling::p[1]'))
    update_problem(identifier=spojId, title=title, url=url, snippet=snippet)
    
def parse_submissions(doc, url):
    spojId = url.split('/status/')[1].split('/signedlist/')[0]
    data = tostring(doc)
    update_user_submissions(identifier=spojId, data=data, url=url)

def parse_user(doc, url):
    spojId = extract_unique_element(doc.xpath('//td/i/font/text()'))
    name = extract_unique_element(doc.xpath("//h3/text()")).replace(u'Informa\xe7\u0151es do ', '').strip()
    country = extract_unique_element(doc.xpath(u"//td[text()='País:']/following-sibling::td[1]/text()"))
    school = extract_unique_element(doc.xpath(u"//td[text()='Instituiçăo:']/following-sibling::td[1]/text()"))
    update_user(identifier=spojId, name=name, country=country, school=school, url=url)

def follow(url):
    logging.debug('follow(' + url + ')')
    for pattern in LINKS_ALLOWED:
        if pattern.search(url):
            if not LINKS_DENIED.search(url):
                return True
        
    return False

class UrlDonloader(webapp.RequestHandler):
    
    def post(self):
        url = self.request.get('url')
        
        logging.debug(WORKER_QUEUE_URL + ' url=' + url)
        
        myqueue = DonloadQueue()
        myqueue.add_follow_func(follow)
        myqueue.add_extract_data_func(re.compile(PROBLENS_PAGE_PATTERN), parse_problem)
        myqueue.add_extract_data_func(re.compile(USERS_PAGE_PATTERN), parse_user)
        myqueue.add_extract_data_func(re.compile(SUBMISSIONS_PAGE_PATTERN), parse_submissions)
        myqueue.add(url)
        
        self.response.write("ok!")
    
    def get(self):
        self.post()
    

application = webapp.WSGIApplication([(WORKER_QUEUE_URL, UrlDonloader)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    
