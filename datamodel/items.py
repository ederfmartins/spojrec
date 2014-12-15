# -*- coding: utf-8 -*-

import scrapy
import datetime

class SpojItem(scrapy.Item):
	_id = scrapy.Field()
	timestamp = scrapy.Field()

class UserItem(SpojItem):
	name = scrapy.Field()
	country = scrapy.Field()
	school = scrapy.Field()
	
class SubmissionsItem(SpojItem):
	data = scrapy.Field()
		
class ProblemItem(SpojItem):
	title = scrapy.Field()
	url = scrapy.Field()
	snippet = scrapy.Field()
	since = scrapy.Field()
	contest = scrapy.Field()

