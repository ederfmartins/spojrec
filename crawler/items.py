# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse
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

def stractUserData(response):
	item = UserItem()
	item['_id'] = response.xpath('//td/i/font/text()').extract()
	item['name'] = response.xpath("//h3/text()").extract()
	item['country'] = response.xpath(u"//td[text()='País:']/following-sibling::td[1]/text()").extract()
	item['school'] = response.xpath(u"//td[text()='Instituiçăo:']/following-sibling::td[1]/text()").extract()
	item['timestamp'] = datetime.datetime.utcnow()
	return item

def stractSubmissionsData(identifier, body):
	item = SubmissionsItem()
	item['_id'] = identifier
	item['data'] = body
	item['timestamp'] = datetime.datetime.utcnow()
	return item	

def stractProblemData(response):
	item = ProblemItem()
	item['_id'] = response.url.split('/problems/')[1].split('/.+')[0].replace('/', '')
	item['title'] = response.xpath('//div[@class="prob"]/table/tr/td/h1/text()').extract()
	item['snippet'] = response.xpath('//p[not(@align)]/text()').extract()
	item['since'] = response.xpath('//td[text()="Data:"]/following-sibling::td[1]/text()')
	item['contest'] = response.xpath('//td[text()="Origem:"]/following-sibling::td[1]/text()')
	item['url'] = response.url
	item['timestamp'] = datetime.datetime.utcnow()
	return item

