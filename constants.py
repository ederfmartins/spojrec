# -*- coding: utf-8 -*-
import os

PRODUCTION = True

CRAWN_SPOJ = '/crawnspojstart'

#SPOJ_URLS = {'BR':'http://br.spoj.com', 'PL':'http://pl.spoj.com'}
SPOJ_URLS = {'BR':'http://br.spoj.com'}

PROBLEM_NAME = '[A-Z0-9]+'
USER_NAME = '[a-z0-9_]+'

#pages of interest
PROBLENS_PAGE_PATTERN = '.*/problems/' + PROBLEM_NAME + '/$'
USERS_PAGE_PATTERN = '.*/users/' + USER_NAME + '/$'
SUBMISSIONS_PAGE_PATTERN = '.*/status/' + USER_NAME + '/signedlist/$'

#default recommender in mencache
DEFAULT_RECOMMENDER = 'defaultRecommender'

def _get_constant(label, replacement):
	if PRODUCTION:
		return os.environ[label]
	else:
		return replacement

#open shift constants
LOG_DIR = _get_constant('OPENSHIFT_PYTHON_LOG_DIR', '~/maratona/spojrec/logs/')
DATA_DIR = _get_constant('OPENSHIFT_DATA_DIR', '~/maratona/spojrec/data')
SCRAPY_BIND_ADDRESS = _get_constant('OPENSHIFT_PYTHON_IP', 'localhost')
SCRAPY_HTTP_PORT = _get_constant('OPENSHIFT_PYTHON_PORT', '8080')
LOGS_DIR = _get_constant('OPENSHIFT_PYTHON_LOG_DIR', '~/maratona/spojrec/logs')
VIRTUAL_ENV_DIR = _get_constant('OPENSHIFT_PYTHON_DIR', '')

#http server
HTTP_HOST = 'localhost'
HTTP_PORT = 8080

#mongodb constants
MONGODB_HOST = _get_constant('OPENSHIFT_MONGODB_DB_HOST', 'localhost')
MONGODB_PORT = _get_constant('OPENSHIFT_MONGODB_DB_PORT', '27017')
MONGODB_URL = 'mongodb://' + MONGODB_HOST + ':' + MONGODB_PORT + '/'
MONGODB_USER = 'admin'
MONGODB_PASS = 'vhZcQNxhPHwe'

