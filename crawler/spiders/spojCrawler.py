# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse, Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log
from scrapy.log import ScrapyFileLogObserver

import re

from crawler.dataExtractor.extractor import *
from crawler.dataExtractor.signedlistParser import parseSignedlist, LABEL_PROBLEM_COLUMN

# Page relationship graph
# <user_data_page> ---> <user_signedlist>
#     ^      
#     |      
#     |      
#     |   <problem_page> <--- <initial_links>
#     |      ^    |        |
#     |      |    |        |
#     |      |    v        |
# <ranks_problem_page> <----
#

SPOJBR_DOMAIN = ("br.spoj.com",)
SPOJ_WORLD_DOMAIN = "www\\.spoj\\.com"

PROBLEM_NAME = '[A-Z0-9]+'
USER_NAME = '[a-z0-9_]+'

#pages of interest
PROBLENS_PAGE_PATTERN = '.*/problems/' + PROBLEM_NAME + '/$'
USERS_PAGE_PATTERN = '.*/users/' + USER_NAME + '/$'
SUBMISSIONS_PAGE_PATTERN = '.*/status/' + USER_NAME + '/signedlist/$'

#links
PROBLEMS_LIST_PATTERN = '.*/problems/[a-z0-9_]+/$'
PROBLEMS_LIST1_PATTERN = '.*/problems/[a-z0-9_]+/sort=0,start=\d+'
PROBLENS_LIST2_PATTERN = '.*/problems/' + PROBLEM_NAME + '/cstart=\d+$'
RANKS_PAGE_PATTERN = '.*/ranks/.*'
RANKS_PAGE_PATTERN_EXCLUDE = '.*/ranks/' + PROBLEM_NAME + '/.*lang=.*'
PROBLENS_PAGE_PATTERN_INCLUDE ='.*/problems/' + PROBLEM_NAME + '/.*cstart=.*'

LINKS_ALLOWED = (PROBLENS_PAGE_PATTERN_INCLUDE, RANKS_PAGE_PATTERN, PROBLEMS_LIST_PATTERN, PROBLEMS_LIST1_PATTERN, PROBLENS_LIST2_PATTERN )
LINKS_DENIED = (RANKS_PAGE_PATTERN_EXCLUDE,)

class SpojCrawler(CrawlSpider):
	name = "spojCrawler"
	contestUnderCrawl = 'BR'
	allowed_domains = SPOJBR_DOMAIN
	start_urls = ["http://br.spoj.com/problems/seletivas", 
	"http://br.spoj.com/problems/contest_noturno/", 
	"http://br.spoj.com/problems/mineira/", 
	"http://br.spoj.com/problems/obi/", 
	"http://br.spoj.com/problems/regionais/",
	"http://br.spoj.com/problems/seletiva_ioi/", 
	"http://br.spoj.com/problems/sulamericana/"]
	#download_delay = 2
	
	rules = (Rule(LinkExtractor(allow=(PROBLENS_PAGE_PATTERN, ), allow_domains=SPOJBR_DOMAIN), callback='parseProblem', follow=True),
	Rule(LinkExtractor(allow=(SUBMISSIONS_PAGE_PATTERN, ), allow_domains=SPOJBR_DOMAIN), callback='parseSubmissions', follow=True),
	Rule(LinkExtractor(allow=(USERS_PAGE_PATTERN, ), allow_domains=SPOJBR_DOMAIN), callback='parseUser', follow=True),
	Rule(LinkExtractor(allow=LINKS_ALLOWED, deny=LINKS_DENIED, allow_domains=SPOJBR_DOMAIN), follow=True, callback='parseLinks'),
	)

	def __init__(self, name=None, **kwargs):
		#ScrapyFileLogObserver(open(self.name + ".log", 'w'), level=log.INFO).start()
		#ScrapyFileLogObserver(open(self.name + "_error.log", 'w'), level=log.ERROR).start()
		
		super(SpojCrawler, self).__init__(name, **kwargs)
		self.spojPattern = re.compile(SPOJ_WORLD_DOMAIN)
		
	def parseProblem(self, response):
		log.msg('Crawling problem url %s.' % response.url, level=log.INFO)
		if self.spojPattern.search(response.url) is None:
			item = extract_problem_data(response)
			if not (item['title'] == 'SPOJ Brasil' or item['title'] == ''):
				return item
	
	def parseSubmissions(self, response):
		identifier = response.url.split('/status/')[1].split('/signedlist/')[0]
		log.msg('Crawling signedlist of user %s from %s.' % (identifier, response.url), level=log.INFO)
		item = extract_submissions_data(identifier, response.body)
		problems = parseSignedlist(item['data'])
		for prob in problems:
			url = str(allowed_domains[0]) + '/problems/' + prob[LABEL_PROBLEM_COLUMN] + '/'
			yield Request(url=url)
		return item
	
	def parseUser(self, response):
		log.msg('Crawling user from %s.' % response.url, level=log.INFO)
		item = extract_user_data(response)
		return item
		
	def parseLinks(self, response):
		log.msg('Crawling link %s.' % response.url, level=log.INFO)
		
	
