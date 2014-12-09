# -*- coding: utf-8 -*-

import datetime
from scrapy.http import Response
from crawler.items import UserItem, SubmissionsItem, ProblemItem

def _extract_unique_element(xpath, joinList=False):
    if joinList and isinstance(xpath, list):
        xpath = ''.join(xpath)
	
    assert (isinstance(xpath, basestring) or len(xpath) <= 1), 'len=' + str(len(xpath)) + ' ' + str(type(xpath)) + ' element=' + str(xpath)
    
    if isinstance(xpath, basestring):
    	return xpath
    elif len(xpath) == 1:
        return xpath[0]
    else:
        return ''

def stract_user_data(response):
	_id = response.xpath('//td/i/font/text()')
	name = response.xpath("//h3/text()")
	country = response.xpath(u"//td[text()='País:']/following-sibling::td[1]/text()")
	school = response.xpath(u"//td[text()='Instituiçăo:']/following-sibling::td[1]/text()")
	
	if isinstance(response, Response):
		_id = _id.extract()
		name = name.extract()
		country = country.extract()
		school = school.extract()
	else:
		_id = _extract_unique_element(_id)
		name = _extract_unique_element(name)
		country = _extract_unique_element(country)
		school = _extract_unique_element(school)
	
	item = UserItem()
	item['_id'] = _id
	item['name'] = name
	item['country'] = country
	item['school'] = school
	item['timestamp'] = datetime.datetime.utcnow()
	return item

def stract_submissions_data(identifier, body):
	item = SubmissionsItem()
	item['_id'] = identifier
	item['data'] = body
	item['timestamp'] = datetime.datetime.utcnow()
	return item	

def stract_problem_data(response, url=None):
	item = ProblemItem()
	
	title = response.xpath('//div[@class="prob"]/table/tr/td/h1/text()')
	snippet = response.xpath('//p[not(@align)]/text()')
	since = response.xpath('//td[text()="Data:"]/following-sibling::td[1]/text()')
	contest = response.xpath('//td[text()="Origem:"]/following-sibling::td[1]/text()')
	
	if url is not None:
		item['_id'] = url.split('/problems/')[1].split('/.+')[0].replace('/', '')
		item['url'] = _extract_unique_element(url)
		item['title'] = _extract_unique_element(title)
		item['snippet'] = _extract_unique_element(snippet, joinList=True)
		item['since'] = _extract_unique_element(since)
		item['contest'] = _extract_unique_element(contest)
	else:
		item['_id'] = response.url.split('/problems/')[1].split('/.+')[0].replace('/', '')
		item['url'] = response.url
		item['title'] = title.extract()
		item['snippet'] = snippet.extract()
		item['since'] = since.extract()
		item['contest'] = contest.extract()
	
	item['timestamp'] = datetime.datetime.utcnow()
	return item
	

