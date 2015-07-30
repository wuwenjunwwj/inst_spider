from scrapy_kernel.spiders.my_crawler import myCrawler
from scrapy_kernel.spiders.my_crawler import my_CrawlerRunner
from scrapy.spiderloader import SpiderLoader
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
class my_spiderManager(SpiderLoader):
    def __init__(self, settings=None):
        SpiderLoader.__init__(self, settings)
        self.spidercls = self.load("scrapy_spider")
        self.craw_runner =my_CrawlerRunner(settings)
        #my_crawler = craw_runner._create_crawler(spidercls)
        #spidercls.set_crawler(my_crawler)
        print "wwj debug in spidermanager",self.spidercls
    def create_crawler(self):
        my_crawler = self.craw_runner._create_crawler(self.spidercls)
        return my_crawler
    @classmethod
    def from_settings(cls, settings):
        print "wwj debug in spidemanger from_setting"
        return cls(settings)
