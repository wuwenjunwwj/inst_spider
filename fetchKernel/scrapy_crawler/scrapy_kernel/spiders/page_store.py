#todo: mutex , pages0,pages1, maxsize
import logging
import time
import os
logger = logging.getLogger(__name__)
class pageStore:
    def __init__(self):
        self.cur_page_index = 0
        self.page_name = 'pages_'
        self.max_size = 8589934592
        pass
    def set_PagePath(self, path):
        self.path = path
        self.fd = os.open( self.path+'/'+self.page_name+str(self.cur_page_index), 
                os.O_RDWR|os.O_CREAT|os.O_APPEND)
        pass
    def set_MaxSize(self, size):
        self.max_size = size

    def write_page(self, url, header, page):
        info = os.fstat(self.fd)
        if(info.st_size > self.max_size):
            self.cur_page_index += 1
            self.fd.close()
            self.fd = os.open( self.path+'/'+self.page_name+str(self.cur_page_index), 
                os.O_RDWR|os.O_CREAT|os.O_APPEND)
        os.write(self.fd, url)
        os.write(self.fd, '\n')
        os.write(self.fd, header)
        os.write(self.fd, '\n\n')
        os.write(self.fd, page)
        os.write(self.fd, '\n')
