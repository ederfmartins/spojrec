#create a data base
mongo <spojrecdb.txt
#crawl spoj data
nohup scrapy crawl spojCrawler -s LOG_FILE=${OPENSHIFT_PYTHON_LOG_DIR}scrapy.log >${OPENSHIFT_PYTHON_LOG_DIR}crawler.log 2>${OPENSHIFT_PYTHON_LOG_DIR}crawler.err
#compute metrics
python recommender/engine.py >${OPENSHIFT_PYTHON_LOG_DIR}metrics.log 2>${OPENSHIFT_PYTHON_LOG_DIR}metrics.err
