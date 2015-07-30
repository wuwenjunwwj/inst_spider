from scrapy.utils.httpobj import urlparse_cached
from scrapy.core.downloader import Downloader
from my_resolver import my_dnscache
class My_Downloader(Downloader):
    def __init__(self, crawler):
        Downloader.__init__(self, crawler)
        pass
    def _get_slot_key(self, request, spider):
        if 'download_slot' in request.meta:
            return request.meta['download_slot']
        host_name = urlparse_cached(request).hostname or ''
        key = my_dnscache.get(host_name)
        print "******************************key----------------",key
        return key

