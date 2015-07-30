# -*- coding: utf-8 -*-

# Scrapy settings for w3school project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_kernel'
SPIDER_LOADER_CLASS = 'scrapy_kernel.spiders.my_spidermanager.my_spiderManager'
SPIDER_MODULES = ['scrapy_kernel.spiders']
NEWSPIDER_MODULE = ''
ITEM_PIPELINES = {  
            'scrapy_kernel.pipelines.ScrapyPipeline':300  
            } 
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0

DUPEFILTER_CLASS = 'bloom_filter.URIBloomFilter'
DUPEFILTER_CAPACITY = '2'
DUPEFILTER_FILENAME ="bloom_filter.dump"
DUPEFILTER_DEBUG = '1'

DEPTH_LIMIT='2'
DEPTH_STATS_VERBOSE='1'
DEPTH_PRIORITY='1'
SPIDER_MIDDLEWARES_BASE = { 
    # Engine side
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50, 
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
    # Spider side
}
EXTENSIONS = {
        'scrapy_kernel.spiders.result_handler.result_handler':500,
        'run_test.SpiderController':50
        }
DOWNLOADER = 'my_downloader.My_Downloader'
DOWNLOADER_MIDDLEWARES = {  
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,  
        'scrapy_kernel.spiders.random_useragent.RandomUserAgentMiddleware' :400  ,
        #'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
        'scrapy_kernel.spiders.retry.DNSRetryMiddleware': None
        }
RETRY_TIME_INTERVAL='60'
PAGE_PATH='data/service'
USER_AGENT_LIST='/search/wuwenjun/project/inst_spider/fetchKernel/scrapy_crawler/scrapy_kernel/spiders/random_user_agent.lst'
DAEMON='True'
#DAEMON='False'
#redis or seeds
SEED_MODE = 'redis' 
SEEDS_FILE='5_seed'
SCHEDULER = 'my_scheduler.my_Scheduler'
#REDIS_CLIENT = 'redis_hanler.redis_client'
