# -*- coding: utf-8 -*-
from spojrec.src.basicdefs import DATA_DIR, SCRAPY_BIND_ADDRESS

if __name__ == '__main__':
   
  config_values = {
    'bind_address': SCRAPY_BIND_ADDRESS,
    'http_port': SCRAPY_HTTP_PORT,
    'logs_dir': LOGS_DIR,
    'eggs_dir': DATA_DIR + 'eggs',
    'dbs_dir': DATA_DIR + 'dbs',
    'items_dir': DATA_DIR + 'items'
  }

  scrapyd_conf = "[scrapyd]\n" + \
    "\n".join('{}={}'.format(key, val) for key, val in config_values.items())
 
  with open('scrapyd.conf', 'w') as f:
    f.write(scrapyd_conf)

  os.system("scrapyd") 
