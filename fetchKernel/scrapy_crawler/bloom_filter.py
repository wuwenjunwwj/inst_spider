from pybloomfilter import BloomFilter
from scrapy.utils.request import request_fingerprint
from scrapy.dupefilters import  BaseDupeFilter
from scrapy.utils.request import request_fingerprint
import logging

#################
#
#overwrite request_seen method
#
################
class URIBloomFilter(BaseDupeFilter):
    def __init__(self, settings, debug = False):
        self.capacity = settings.getint("DUPEFILTER_CAPACITY")
        self.filename = settings.get("DUPEFILTER_FILENAME")
        self.debug = debug
        self.error_rate = 0.01
        self.logger = logging.getLogger(__name__)
        self.bloom_filter_ =BloomFilter(self.capacity, self.error_rate, self.filename) 
    
    @classmethod
    def from_settings(cls, settings):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(settings, debug)
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if self.check(fp):
            return True
        else:
            self.insert(fp)

    ###-------todo-------##
    def request_fingerprint(self, request):
        return request_fingerprint(request)
    
    def check(self, request):

        ret = request in self.bloom_filter_
        return ret
    
    def insert(self, request):
        self.bloom_filter_.add(request)
        #print len(self.bloom_filter_)
        #print self.bloom_filter_.hash_seeds
        #print self.bloom_filter_.num_bits
        #print self.bloom_filter_.num_hashes
    
    def reset(self):
        self.bloom_filter_.clear_all()
    
    def save(self):
        pass
    def load(self):
        self.bloom_filter_.sync()
        self.bloom_filter_.open("bloom.dump") 
        pass
    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)

