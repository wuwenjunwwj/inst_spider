# -*-coding:utf-8-*-  
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import logging
from scrapy import signals

logger = logging.getLogger(__name__) 
class RandomUserAgentMiddleware(UserAgentMiddleware):  
  
    def __init__(self,settings, user_agent=''):
        self.user_agent = user_agent
        user_agent_list_file = settings.get('USER_AGENT_LIST')
        if not user_agent_list_file:
            ua = settings.get('USER_AGENT', user_agent)
            self.user_agent_list = [ua]
        else:
            with open(user_agent_list_file, 'r') as f:
                self.user_agent_list = [line.strip() for line in f.readlines()]
    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        return obj
    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)  
        if ua:  
            #logger.info('Current UserAgent: '+ua)  
            request.headers.setdefault('User-Agent', ua)  
