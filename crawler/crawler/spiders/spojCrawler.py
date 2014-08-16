# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log
from scrapy.log import ScrapyFileLogObserver

import re

from crawler.items import *

SPOJBR_DOMAIN = ("br.spoj.com",)
SPOJ_WORLD_DOMAIN = "www\\.spoj\\.com"
RULE_EXPRESSION_PROBLENS = '.*/problems/[A-Z0-9]+/$'
RULE_EXPRESSION_USERS = '.*/users/[a-z0-9_]+/'
RULE_EXPRESSION_SUBMISSIONS = '.*/status/.+/signedlist/.*'

RULE_EXPRESSION_PROBLENS_SEARCH = '.*/problems/.*'

RULE_EXPRESSION_STATUS = '.*/status/.*'
RULE_EXPRESSION_STATUS_USER = '.*/status/[a-z0-9_]/all/.*'
RULE_EXPRESSION_STATUS_PROBLENS_BY_USER = '.*/status/[A-Z0-9]+,[a-z0-9_]+/'

RULE_EXPRESSION_RANKS = '.*/ranks/.*'
RULE_EXPRESSION_RANKS_LANGUAGE = '.*/ranks/[A-Z0-9]+/.*lang=.*'

class SpojCrawler(CrawlSpider):
	name = "spojCrawler"
	allowed_domains = SPOJBR_DOMAIN
	start_urls = ["http://br.spoj.com/ranks/"]
	#download_delay = 2
	
	rules = (Rule(LinkExtractor(allow=(RULE_EXPRESSION_PROBLENS_SEARCH, ), allow_domains=SPOJBR_DOMAIN), callback='parseProblem', follow=True),
	Rule(LinkExtractor(allow=(RULE_EXPRESSION_SUBMISSIONS, ), allow_domains=SPOJBR_DOMAIN), callback='parseSubmissions', follow=True),
	Rule(LinkExtractor(allow=(RULE_EXPRESSION_USERS, ), allow_domains=SPOJBR_DOMAIN), callback='parseUser', follow=True),
	
	Rule(LinkExtractor(allow=(RULE_EXPRESSION_STATUS, RULE_EXPRESSION_RANKS ), deny=(RULE_EXPRESSION_SUBMISSIONS, RULE_EXPRESSION_STATUS_PROBLENS_BY_USER, RULE_EXPRESSION_STATUS_USER, RULE_EXPRESSION_RANKS_LANGUAGE), allow_domains=SPOJBR_DOMAIN), callback='parseStatus', follow=True))

	def __init__(self, name=None, **kwargs):
		ScrapyFileLogObserver(open(self.name + ".log", 'w'), level=log.INFO).start()
		ScrapyFileLogObserver(open(self.name + "_error.log", 'w'), level=log.ERROR).start()
		
		super(SpojCrawler, self).__init__(name, **kwargs)
		self.problemPattern = re.compile(RULE_EXPRESSION_PROBLENS)
		self.spojPattern = re.compile(SPOJ_WORLD_DOMAIN)
		
	def parseProblem(self, response):
		log.msg('Crawling problem url %s.' % response.url, level=log.INFO)
		if (not self.problemPattern.search(response.url) == None) and (self.spojPattern.search(response.url) == None):
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
		
	def parseStatus(self, response):
		log.msg('Crawling %s.' % response.url, level=log.INFO)
	
