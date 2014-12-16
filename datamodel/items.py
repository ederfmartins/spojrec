# -*- coding: utf-8 -*-

import scrapy
import datetime

class SpojItem(scrapy.Item):
	_id = scrapy.Field()
	timestamp = scrapy.Field()

class UserItem(SpojItem):
	"""Store data about users of spoj"""
	name = scrapy.Field()
	country = scrapy.Field()
	school = scrapy.Field()
	
class SubmissionsItem(SpojItem):
	"""Store data about problems submited to spoj"""
	data = scrapy.Field()
		
class ProblemItem(SpojItem):
	"""Store data about problems of spoj"""
	title = scrapy.Field()
	url = scrapy.Field()
	snippet = scrapy.Field()
	since = scrapy.Field()
	contest = scrapy.Field()

