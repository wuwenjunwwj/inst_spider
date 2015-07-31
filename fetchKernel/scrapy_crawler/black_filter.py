import logging
from os import path
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy.http import Request
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.log import failure_to_exc_info
from six.moves.urllib.parse import urlparse
logger = logging.getLogger(__name__)
class DomainFilterMiddleware(object):
    def __init__(self, crawler):
        #if not crawler.settings.get('DomainFilter'):
        #    raise NotConfigured
        self.domain_filter_file = crawler.settings.get('DomainFilter')
        self.domain_filter_file = 'domain.lst'
        self.crawler = crawler
        self.domain_dict = self.load_domainfilter()
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    
    def process_request(self, request, spider):
        domain = self.domain_parse(request)
        if (domain  in self.domain_dict) and self.domain_dict[domain]=='DISALLOWED':
            logger.debug("Forbidden by DomainFilter: %(request)s",
                    {'request': request}, extra={'spider': spider})
        raise IgnoreRequest

    def domain_parse(self, request):
        o = urlparse(request.url)
        if o.netloc:
            site = o.netloc.split(":")[0]
            ##todo
            domain = site
            return domain
    def load_domainfilter(self):
        if not path.exists(self.domain_filter_file):
            raise NotConfigured("Can't find " + self.domain_filter_file)
        domain_dict = {}
        delimite=' '
        with open(self.domain_filter_file, 'r') as f:
            for line in f.readlines():
                if len(line.split(delimite)) >=2:
                    domain = line.split(delimite)[0].strip()
                    rule = line.split(delimite)[1].strip() 
                    if rule =='DISALLOWED' or rule == 'ALLOWED':
                        domain_dict[domain] = rule
                else:
                    logger.info("load_domainfilter pass the wrong line")
        return domain_dict
