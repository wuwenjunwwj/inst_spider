from twisted.internet import defer
from twisted.internet.base import ThreadedResolver
from scrapy.utils.datatypes import LocalCache


my_dnscache = LocalCache(10000)
class my_CachingThreadedResolver(ThreadedResolver):
    def __init__(self, reactor, cache_size, timeout):
        super(my_CachingThreadedResolver, self).__init__(reactor)
        my_dnscache.limit = cache_size
        self.timeout = timeout
    def getHostByName(self, name, timeout=None):
        if name in my_dnscache:
            return defer.succeed(my_dnscache[name])
        if not timeout:
            timeout = self.timeout
        d = super(my_CachingThreadedResolver, self).getHostByName(name, timeout)
        d.addCallback(self._cache_result, name)
        return d

    def _cache_result(self, result, name):
        my_dnscache[name] = result
        return result

