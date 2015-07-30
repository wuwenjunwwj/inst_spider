# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#project: w3school  
#file   : items.py  
#author : younghz  
#brief  : define W3schoolItem.  
  
from scrapy.item import Item,Field  
  
class HtmlItem(Item):
    article_name = Field()
    article_url = Field()
