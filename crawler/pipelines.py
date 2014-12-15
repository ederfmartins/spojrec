# -*- coding: utf-8 -*-

import os
import scrapy
from scrapy import log

from datamodel.items import UserItem, SubmissionsItem, ProblemItem
from datamodel.database import Database

class UserscrawlerPipeline(object):
	def open_spider(self, spider):
		log.msg('Connecting to mongodb.', level=log.INFO)
		self.database = Database(spider.contestUnderCrawl)

	def process_item(self, item, spider):
		log.msg('Adding %s to mongodb.' % item['_id'], level=log.INFO)
	
		if type(item) is UserItem:
			self.database.update_user(dict(item))
		elif type(item) is SubmissionsItem:
			self.database.update_submission_data(dict(item))
		elif type(item) is ProblemItem:
			self.database.update_problem(dict(item))
		
