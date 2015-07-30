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
        fd = os.open( self.path+'/'+self.page_name+str(self.cur_page_index), 
                os.O_RDWR|os.O_CREAT|os.O_APPEND)
        pass
    def set_MaxSize(self, size):
        self.max_size = size

    def write_page(self, url, header, page):
        info = os.fstat(fd)
        if(info.st_size > self.max_size):
            self.cur_page_index += 1
            fd.close()
            fd = os.open( self.path+'/'+self.page_name+str(self.cur_page_index), 
                os.O_RDWR|os.O_CREAT|os.O_APPEND)
        os.write(fd, url)
        os.write(fd, '\n')
        os.write(fd, header)
        os.write(fd, '\n\n')
        os.write(fd, page)
