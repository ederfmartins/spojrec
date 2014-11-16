# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from scrapy import log

from items import *
from dataExtractor.signedlistParser import parseSignedlist

import pymongo
from pymongo import MongoClient
#from bson import ObjectId

class UserscrawlerPipeline(object):
	def __init__(self):
		host = os.environ['OPENSHIFT_MONGODB_DB_HOST']
        port = os.environ['OPENSHIFT_MONGODB_DB_PORT']
        self.client = MongoClient('mongodb://' + host + ':' + port + '/')
        self.client.index.authenticate('admin', 'vhZcQNxhPHwe', mechanism='MONGODB-CR')
        self.db = self.client.index

	def process_item(self, item, spider):
		log.msg('Adding %s to mongodb.' % item['spojId'], level=log.INFO)
	
		if type(item) is UserItem:
			self.db.users.insert(dict(item))
		elif type(item) is SubmissionsItem:
			#storing full history data
			self.db.submissionData.insert(dict(item))
			
			#storing parsed user submission data
			solvedProblems = []
			
			for problem in parseSignedlist(item['data']):
				if problem['RESULT'] == 'AC':
					solvedProblems.append(problem['PROBLEM'])
			
			self.db.solvedProblems.insert(dict({'spojId':item['spojId'], 'problemList':solvedProblems}))
		elif type(item) is ProblemItem:
			self.db.problems.insert(dict(item))
		
