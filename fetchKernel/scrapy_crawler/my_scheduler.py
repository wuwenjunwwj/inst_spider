import logging
import os
import json
import logging
import time
from os.path import join, exists
from scrapy import signals
from queuelib import PriorityQueue
from scrapy.utils.reqser import request_to_dict, request_from_dict
from scrapy.utils.misc import load_object
from scrapy.utils.job import job_dir

from scrapy.core.scheduler import Scheduler
from redis_handler import redis_handler
from scrapy.http import Request
from queuelib import PriorityQueue
logger = logging.getLogger(__name__)

def test():
    print "----------------------just for test-------------------------"

class my_Scheduler(Scheduler):
    def __init__(self, dupefilter, jobdir=None, dqclass=None, mqclass=None, logunser=False, stats=None,run_as_daemon=False):
        self.df = dupefilter
        self.dqdir = self._dqdir(jobdir)
        self.dqclass = dqclass
        self.mqclass = mqclass
        self.logunser = logunser
        self.stats = stats
        self.run_as_daemon = run_as_daemon
        self.dqs = None 
        self.mqs = PriorityQueue(self._newmq)
        #Scheduler.__init__(self, dupefilter, jobdir, dqclass, mqclass, logunser, stats)
        self.redis_handler = redis_handler('localhost', 6379, 0)
        self.redis_handler.connect_db()
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        run_as_daemon = settings.get('DAEMON')
        if(run_as_daemon):
            crawler.signals.connect(test, signal=signals.spider_idle)
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        dqclass = load_object(settings['SCHEDULER_DISK_QUEUE'])
        mqclass = load_object(settings['SCHEDULER_MEMORY_QUEUE'])
        logunser = settings.getbool('LOG_UNSERIALIZABLE_REQUESTS')
        return cls(dupefilter, job_dir(settings), dqclass, mqclass, logunser, crawler.stats, run_as_daemon)
    #def has_pending_requests(self):
    #    if(self.run_as_daemon):
    #        return len(self) >= 0
    #    else:
    #        return len(self) > 0
    def open(self, spider):
        self.spider = spider
        self.mqs = PriorityQueue(self._newmq)
        self.dqs = self._dq() if self.dqdir else None
        self.enqueue()
        return self.df.open()
    def _newmq(self, priority):
        return self.mqclass()
    def close(self, reason):
        if self.dqs:
            prios = self.dqs.close()
            with open(join(self.dqdir, 'active.json'), 'w') as f:
                json.dump(prios, f)
        return self.df.close(reason)
    def enqueue(self):
        #while(1):
        #value = 'http://www.wuwenjuncsdn.net'
        value = 'http://www.baidu.com'
        print "---------------------baidu.com in queue"
            #value = self.redis_handler.read('key-wwj')
        dont_filter = True
        request = Request(value, dont_filter)
        ret = self.enqueue_request(request)
        time.sleep(1)
        value = 'https://www.baidu.com/s?wd=11&ie=utf-8&cl=3&t=12&fr=news'
        request = Request(value, dont_filter)
        ret = self.enqueue_request(request)
        value = 'https://www.baidu.com/s?wd=12&ie=utf-8&cl=3&t=12&fr=news'
        request = Request(value, dont_filter)
        ret = self.enqueue_request(request)
        value = 'https://www.baidu.com/s?wd=13&ie=utf-8&cl=3&t=12&fr=news'
        request = Request(value, dont_filter)
        value = 'https://www.baidu.com/s?wd=14&ie=utf-8&cl=3&t=12&fr=news'
        ret = self.enqueue_request(request)
        value = 'https://www.baidu.com/s?wd=15&ie=utf-8&cl=3&t=12&fr=news'
        request = Request(value, dont_filter)
        ret = self.enqueue_request(request)
        value = 'https://www.baidu.com/s?wd=16&ie=utf-8&cl=3&t=12&fr=news'
        request = Request(value, dont_filter)
        ret = self.enqueue_request(request)
        value = 'http://www.baidu.com/6.html'
        request = Request(value, dont_filter)
        ret = self.enqueue_request(request)
        value = 'http://www.baidu.com/7.html'
        request = Request(value, dont_filter)
        time.sleep(1)
        ret = self.enqueue_request(request)
        value = 'http://www.baidu.com/8.html'
        request = Request(value, dont_filter)
        ret = self.enqueue_request(request)
