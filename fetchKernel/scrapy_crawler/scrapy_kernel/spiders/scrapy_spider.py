#!/usr/bin/python  
# -*- coding:utf-8 -*-  
import os
import scrapy
from scrapy import signals 
from scrapy.spiders import Spider  
from scrapy.utils.datatypes import MultiValueDict  
from scrapy.selector import Selector  
import logging  
from scrapy.http import Request
from scrapy_kernel.items import HtmlItem  
from scrapy_kernel.spiders.my_crawler import myCrawler  
from scrapy_kernel.spiders.my_spidermanager import my_spiderManager  
from scrapy_kernel.spiders.page_store import *  
from scrapy.utils.misc import load_object
FORMAT = '%(asctime)-15s'
logger = logging.getLogger(__name__)
from multiprocessing import Process
class ScrapySpider(Spider):  
    name = "scrapy_spider"
    #allowed_domains = ["blog.csdn.net"] 

    def __init__(self, crawler, *args, **kwargs):
        print "wwj debug in scrapy spider init"
        Spider.__init__(self, name=None, **kwargs)
        self.seed_mode= crawler.settings.get('SEED_MODE')
        if(self.seed_mode == 'seeds'):
            seeds_file = crawler.settings.get('SEEDS_FILE')
            self.load_seeds(seeds_file)
        elif (self.seed_mode == 'redis'):
            redis_client_path = crawler.settings.get('REDIS_CLIENT')
            #self.redis_client_cls = load_object(redis_client_path)
            #self.start_client()
    
    def load_seeds(self, seeds_file):
        if not seeds_file:
            print "just pass"
            pass
        else:
            with open(seeds_file, 'r') as f:
                #self.start_urls = [line.strip() for line in f.readlines()]
                pass                                                                        

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        logger.info("wwj debug in spider from_crawler")
        obj = cls(crawler, *args, **kwargs)
        #----miss this
        obj._set_crawler(crawler)
        return obj
    def start_client(self):
        p = Process(target = self.redis_client_cls.start, args = ())
        print 'Process will start.'
        p.start()
        p.join()
    #def start_requests(self):
    #    yield scrapy.Request('http://www.csdn---wwjtest.net/', self.parse)
