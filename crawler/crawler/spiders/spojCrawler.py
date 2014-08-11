# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log
from scrapy.log import ScrapyFileLogObserver

import re

from crawler.items import *

RULE_EXPRESSION_PROBLENS = '.*/problems/[A-Z0-9]+/$'
RULE_EXPRESSION_PROBLENS_SEARCH = '.*/problems/.*'
RULE_EXPRESSION_SUBMISSIONS = '.*/status/.+/signedlist/.*'
RULE_EXPRESSION_USERS = '.*/users/.*/'

class SpojCrawler(CrawlSpider):
	name = "spojCrawler"
	allowed_domains = ["br.spoj.com"]
	start_urls = ["http://br.spoj.com/ranks/"]
	download_delay = 2
	
	rules = (Rule(LinkExtractor(allow=(RULE_EXPRESSION_PROBLENS_SEARCH, )), callback='parseProblem', follow=True),
	Rule(LinkExtractor(allow=(RULE_EXPRESSION_SUBMISSIONS, )), callback='parseSubmissions', follow=True),
	Rule(LinkExtractor(allow=(RULE_EXPRESSION_USERS, )), callback='parseUser', follow=True))

	def __init__(self, name=None, **kwargs):
		ScrapyFileLogObserver(open(self.name + ".log", 'w'), level=log.INFO).start()
		ScrapyFileLogObserver(open(self.name + "_error.log", 'w'), level=log.ERROR).start()
		
		super(SpojCrawler, self).__init__(name, **kwargs)
		self.problemPattern = re.compile(RULE_EXPRESSION_PROBLENS)
		
	def parseProblem(self, response):
		log.msg('Crawling problem url %s.' % response.url, level=log.INFO)
		if not self.problemPattern.search(response.url) == None:
			item = stractProblemData(response)
			if not (item['title'] == 'SPOJ Brasil' or item['title'] == ''):
				return item
	
	def parseSubmissions(self, response):
		identifier = response.url.split('/status/')[1].split('/signedlist/')[0]
		log.msg('Crawling signedlist of user %s from %s.' % (identifier, response.url), level=log.INFO)
		item = stractSubmissionsData(identifier, response.body)
		return item
	
	def parseUser(self, response):
		log.msg('Crawling user from %s.' % response.url, level=log.INFO)
		item = stractUserData(response)
		return item
	
