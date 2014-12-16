# -*- coding: utf-8 -*-
import sys
import subprocess
from subprocess import PIPE

from constants import LOGS_DIR

#create a data base
print subprocess.Popen("mongo <spojrecdb.txt", shell=True, stdout=PIPE).stdout.read()

#crawl spoj data
print subprocess.Popen("scrapy crawl spojCrawler -s LOG_FILE=" + LOGS_DIR + "scrapy.log 2>" + LOGS_DIR + "scrapy.err", shell=True, stdout=PIPE).stdout.read()

#compute metrics
print subprocess.Popen("python recommender/metrics.py BR >" + LOGS_DIR + "metrics.log 2>" + LOGS_DIR + "metrics.err", shell=True, stdout=PIPE).stdout.read()
