from twisted.internet import reactor, defer
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy_kernel.spiders.scrapy_spider import ScrapySpider
from scrapy.utils.project import inside_project, get_project_settings
from scrapy import signals
import time

class SpiderController(object):
    def __init__(self, crawler):
        self.crawler = crawler
        crawler.signals.connect(self.launch_spiders, signal=signals.engine_started)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def launch_spiders(self):
        pass
        #settings = get_project_settings()
        #spider = ScrapySpider(self.crawler, 'scrapy_spider')
        #for s in self.crawler.engine.open_spiders:
        #    self.crawler.engine.scraper.close_spider(s) 
        #for s in self.crawler.engine.open_spiders:
        #    self.crawler.engine.close_spider(s, reason='shutdown') 
        #time.sleep(5)
        #print "*********************wwj debug in launch_spiders"
        #self.crawler.engine.scraper.open_spider(spider)
