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


class my_Scheduler(Scheduler):
    def __init__(self, crawler, dupefilter, jobdir=None, dqclass=None, mqclass=None, logunser=False, stats=None,run_as_daemon=False):
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
        crawler.signals.connect(self.enqueue, signal=signals.request_scheduled)
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        run_as_daemon = settings.get('DAEMON')
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        dqclass = load_object(settings['SCHEDULER_DISK_QUEUE'])
        mqclass = load_object(settings['SCHEDULER_MEMORY_QUEUE'])
        logunser = settings.getbool('LOG_UNSERIALIZABLE_REQUESTS')
        return cls(crawler, dupefilter, job_dir(settings), dqclass, mqclass, logunser, crawler.stats, run_as_daemon)
    
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

    def schedule_next_request(self):
        """Schedules a request if available"""
        dont_filter=True
        for key in self.redis_handler.r.scan_iter(match='*', count=1):
            print key
            return Request(key, dont_filter)
    def enqueue(self):
        print "enqueue"
        request = self.schedule_next_request()
        if(request):
            self.enqueue_request(request)
        request1 = Request("http://www.baidu.com:80/a", False)
        print "wwj debug before enqueue_request"
        self.enqueue_request(request1)

