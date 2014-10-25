
import logging
from operator import isCallable

from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from google.appengine.api import memcache

from basicdefs import WORKER_QUEUE_URL

from lxml.html import parse
from urllib2 import urlopen

_DOWNLOADED = 'D'
_ON_QUEUE = 'Q'

class DonloadQueue:
    
    def __init__(self):
        self.extractDataFunc = dict()
        self.followFunc = None
        self.memcacheClient = memcache.Client()

    def add_follow_func(self, followFunc):
        """set the callback func that determine if a url needed be followed."""
        assert isCallable(followFunc)
        logging.debug('add ' + followFunc.__name__ + ' has a follow_func callback')
        self.followFunc = followFunc
    
    def add_extract_data_func(self, urlPattern, func):
        """Map func has the extracted data func to urlPattern"""
        assert isCallable(func)
        logging.debug('add ' + func.__name__ + ' has callback for ' + str(urlPattern))
        self.extractDataFunc[urlPattern] = func

    def need_download(self, url):
        """Verify if a url need to be downloaded."""
        #result = DonloadQueueRecord.query(DonloadQueueRecord.url == url).fetch()
        #logging.debug('need_download(' + url + ') len =' + str(len(result)))
        #return len(result) == 0
        needDownload = True
        storedUrl = self.memcacheClient.gets(url)
        
        if not storedUrl is None:
            if storedUrl == _DOWNLOADED:
                needDownload = False
        
        logging.debug('need_download(' + url + ') =' + str(needDownload))
        return needDownload
    
    def wait_for_download(self, url):
        wait = False
        storedUrl = self.memcacheClient.gets(url)
        
        if not storedUrl is None:
            wait = True
        
        logging.debug('need_download(' + url + ') =' + str(wait))
        return wait
    
    def add_to_gQueue(self, url):
        if not self.wait_for_download(url):
            taskqueue.add(url=WORKER_QUEUE_URL, params={'url': url})
            self.memcacheClient.add(key=url, value=_ON_QUEUE, time=5*3600)
            
    
    def mark_as_downloaded(self, theUrl):
        #DonloadQueueRecord(url=theUrl).put()
        self.memcacheClient.add(key=theUrl, value=_DOWNLOADED, time=5*3600)
    
    def clean_url_list(self):
        """limpar a entidade que armazena as urls."""
        #ndb.delete_multi(DonloadQueueRecord.query().fetch(keys_only=True))
        pass
    
    def add(self, url):
        """Add the url to the queue"""
        
        logging.debug('add(' + url + ')')
        
        if self.need_download(url):
            if self.followFunc is None or self.followFunc(url):
                doc = self.download(url)
                doc.make_links_absolute(url)
                self.extract_data(doc, url)
                self.mark_as_downloaded(url)
                self.link_extractor(doc)
    
    def link_extractor(self, doc):
        """Extract links from doc(with the links in absolute form)."""
        #considerar usar doc.iterlinks()
        links = doc.xpath('//a/@href')
        extracted = []
        for link in links:
            if self.followFunc is None:
                extracted.append(link)
                self.add_to_gQueue(link)
            else:
                if self.followFunc(link):
                    if self.need_download(link):
                        extracted.append(link)
                        self.add_to_gQueue(link)
                        
        logging.debug('link_extractor(' + str(extracted) + ')')
    
    def extract_data(self, doc, url):
        for pattern in self.extractDataFunc:
            if pattern.match(url):
                callback = self.extractDataFunc[pattern]
                if isCallable(callback):
                    logging.debug('extract_data(' + url + ', ' + callback.__name__ + ')')
                    callback(doc, url)
    
    def download(self, url):
        logging.debug('download(' + url + ')')
        page = urlopen(url)
        return parse(page).getroot()

    def restart(self, seeds):
        """Restart the crawler."""
        logging.debug('restart(' + str(seeds) + ')')
        self.clean_url_list()
        for url in seeds:
            self.add(url)
            
class DonloadQueueRecord(ndb.Model):
    """To check if a url is already downloaded"""
    url = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
