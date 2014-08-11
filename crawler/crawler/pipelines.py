# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy import log

from items import *
from dataExtractor.signedlistParser import parseSignedlist

import pymongo
from pymongo import MongoClient

class UserscrawlerPipeline(object):
	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.spojrec

	def process_item(self, item, spider):
		log.msg('Adding %s to mongodb.' % item['spojId'], level=log.INFO)
	
		if type(item) is UserItem:
			self.db.users.insert(dict(item))
		elif type(item) is SubmissionsItem:
			solvedProblems = []
			
			for problem in item['data']:
				if problem['RESULT'] == 'AC':
					solvedProblems.append(problem['PROBLEM'])
			
			self.db.solvedProblems.insert(dict({'spojId':item['spojId'], 'problemList':solvedProblems}))
			self.db.submissionData.insert(dict(item))
		elif type(item) is ProblemItem:
			self.db.problems.insert(dict(item))
		
