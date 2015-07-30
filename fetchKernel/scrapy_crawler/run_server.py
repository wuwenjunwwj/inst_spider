from twisted.internet import reactor, defer
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy_kernel.spiders.scrapy_spider import ScrapySpider
from scrapy.utils.project import inside_project, get_project_settings
from my_resolver import my_CachingThreadedResolver
class my_CrawlerProcess(CrawlerProcess):
    def __init__(self, settings=None):
        super(my_CrawlerProcess, self).__init__(settings)

    def _get_dns_resolver(self):
        if self.settings.getbool('DNSCACHE_ENABLED'):
            cache_size = self.settings.getint('DNSCACHE_SIZE')
        else:
            cache_size = 0
        print "wwj debug return my_cachingThreadedResolver"
        return my_CachingThreadedResolver(
            reactor=reactor,
            cache_size=cache_size,
            timeout=self.settings.getfloat('DNS_TIMEOUT')
        )


settings = get_project_settings()
my_process = my_CrawlerProcess(settings)

runner = CrawlerRunner(settings)
#### one runner, more spiders 
spidercls = runner.spider_loader.load('scrapy_spider')
my_crawler = runner._create_crawler(spidercls)
my_crawler.spider = my_crawler._create_spider('scrapy_spider')
my_crawler.engine = my_crawler._create_engine()

start_requests = iter(my_crawler.spider.start_requests())
close_if_idle = False
my_crawler.engine.open_spider(my_crawler.spider, start_requests, close_if_idle)
my_crawler.engine.start()

#process.crawl('scrapy_spider')
stop_after_crawl = False
my_process.start(stop_after_crawl)
