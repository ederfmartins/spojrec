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
from constants import MONGODB_URL, MONGODB_USER, MONGODB_PASS

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

#TODO: MUDAR FORMA QUE GUARDA NO DB db.teste.update({'_id' : x}, {'_id':x, 'value':'teste eder'}, upsert=True)
#x = ObjectId("507f1f77bcf86cd799439011")
class UserscrawlerPipeline(object):
	def __init__(self):
		self.client = MongoClient(MONGODB_URL)
		self.client.index.authenticate(MONGODB_USER, MONGODB_PASS, mechanism='MONGODB-CR')
		self.db = self.client.index

	def process_item(self, item, spider):
		log.msg('Adding %s to mongodb.' % item['_id'], level=log.INFO)
	
		if type(item) is UserItem:
			self.db.users.update({'_id' : item["_id"]}, dict(item), upsert=True)
		elif type(item) is SubmissionsItem:
			self.db.submissionData.update({'_id' : item["_id"]}, dict(item), upsert=True)
		elif type(item) is ProblemItem:
			self.db.problems.update({'_id' : item["_id"]}, dict(item), upsert=True)
		
