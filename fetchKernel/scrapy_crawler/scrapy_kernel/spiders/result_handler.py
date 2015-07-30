from scrapy import signals
from scrapy_kernel.spiders.page_store import *
class result_handler():
    def __init__(self, crawler):
        crawler.signals.connect(self.handle_result, signal=signals.response_received)
        self._page_path = crawler.settings.get('PAGE_PATH')
        if not os.path.exists(self._page_path):
            print "set path error"
        else:
            self._page_store = pageStore()
            self._page_store.set_PagePath(self._page_path)
            pass
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    def handle_result(self, response):
        fetch_time = time.asctime(time.localtime(time.time()))
        print "write result to local pages"
        meta_header= response.headers
        meta_header.setlist('Fetch-Time', fetch_time)
        self._page_store.write_page(response._url, meta_header.to_string(), response._body)

