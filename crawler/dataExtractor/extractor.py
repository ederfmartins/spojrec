# -*- coding: utf-8 -*-

import datetime
from scrapy.http import Response
from datamodel.items import UserItem, SubmissionsItem, ProblemItem

def _extract_unique_element(xpath, joinList=False):
    if joinList and isinstance(xpath, list):
        xpath = '\n'.join(xpath)
	
    assert (isinstance(xpath, basestring) or len(xpath) <= 1), 'len=' + str(len(xpath)) + ' ' + str(type(xpath)) + ' element=' + str(xpath)
    
    if isinstance(xpath, basestring):
    	return xpath
    elif len(xpath) == 1:
        return xpath[0]
    else:
        return ''

def extract_user_data(response):
	_id = response.xpath('//td/i/font/text()')
	name = response.xpath("//h3/text()")
	country = response.xpath(u"//td[text()='País:']/following-sibling::td[1]/text()")
	school = response.xpath(u"//td[text()='Instituiçăo:']/following-sibling::td[1]/text()")
	
	if isinstance(response, Response):
		_id = _extract_unique_element(_id.extract())
		name = _extract_unique_element(name.extract())
		country = _extract_unique_element(country.extract())
		school = _extract_unique_element(school.extract())
	else: #etree getroot
		_id = _extract_unique_element(_id)
		name = _extract_unique_element(name)
		country = _extract_unique_element(country)
		school = _extract_unique_element(school)
	
	item = UserItem()
	item['_id'] = _id
	item['name'] = name.replace(u'Informa\xe7\u0151es do ', '').strip()
	item['country'] = country
	item['school'] = school
	item['timestamp'] = datetime.datetime.utcnow()
	return item

def extract_submissions_data(identifier, body):
	item = SubmissionsItem()
	item['_id'] = identifier
	item['data'] = body
	item['timestamp'] = datetime.datetime.utcnow()
	return item	

def extract_problem_data(response, url=None):
	item = ProblemItem()
	
	title = response.xpath('//div[@class="prob"]/table/tr/td/h1/text()')
	snippet = response.xpath('//p/text()')
	since = response.xpath('//td[text()="Data:"]/following-sibling::td[1]/text()')
	contest = response.xpath('//td[text()="Origem:"]/following-sibling::td[1]/text()')
	
	if url is not None:
		item['_id'] = url.split('/problems/')[1].split('/.+')[0].replace('/', '')
		item['url'] = _extract_unique_element(url)
		item['title'] = _extract_unique_element(title)
		item['snippet'] = _extract_unique_element(snippet, joinList=True)
		item['since'] = _extract_unique_element(since)
		item['contest'] = _extract_unique_element(contest)
	elif isinstance(response, Response):
		item['_id'] = response.url.split('/problems/')[1].split('/.+')[0].replace('/', '')
		item['url'] = response.url
		item['title'] = _extract_unique_element(title.extract())
		item['snippet'] = _extract_unique_element(snippet.extract(), joinList=True)
		item['since'] = _extract_unique_element(since.extract())
		item['contest'] = _extract_unique_element(contest.extract())
	
	item['timestamp'] = datetime.datetime.utcnow()
	return item
	

