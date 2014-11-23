# -*- coding: utf-8 -*-
import os

CRAWN_SPOJ = '/crawnspojstart'

WORKER_QUEUE_URL = '/urldownloader'

PROBLEM_NAME = '[A-Z0-9]+'
USER_NAME = '[a-z0-9_]+'

#pages of interest
PROBLENS_PAGE_PATTERN = '.*/problems/' + PROBLEM_NAME + '/$'
USERS_PAGE_PATTERN = '.*/users/' + USER_NAME + '/$'
SUBMISSIONS_PAGE_PATTERN = '.*/status/' + USER_NAME + '/signedlist/$'

#default recommender in mencache
DEFAULT_RECOMMENDER = 'defaultRecommender'


#open shift constants
DATA_DIR = os.environ['OPENSHIFT_DATA_DIR']
SCRAPY_BIND_ADDRESS = os.environ['OPENSHIFT_PYTHON_IP']
SCRAPY_HTTP_PORT = os.environ['OPENSHIFT_PYTHON_PORT']
LOGS_DIR = os.environ['OPENSHIFT_PYTHON_LOG_DIR']

#mongodb constants
MONGODB_HOST = os.environ['OPENSHIFT_MONGODB_DB_HOST']
MONGODB_PORT = os.environ['OPENSHIFT_MONGODB_DB_PORT']
MONGODB_URL = 'mongodb://' + MONGODB_HOST + ':' + MONGODB_PORT + '/'
MONGODB_USER = 'admin'
MONGODB_PASS = 'vhZcQNxhPHwe'
