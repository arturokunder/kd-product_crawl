# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exceptions import DropItem

from pymongo import MongoClient


MONGO_DB = {
    'NAME': 'heroku_app19278317',
    'USER': 'crawler',
    'PASSWORD': 'product_crawler',
    'HOST': 'ds053198.mongolab.com',
    'PORT': 53198,
}

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class DropDuplicateItemPipeline(object):
    def __init__(self):
        self.sku_seen = set()
    def process_item(self, item, spider):
        
        if item['tienda'] + str(item['sku']) in self.sku_seen:
            raise DropItem("Duplicate link: %s" % (item['tienda'] + str(item['sku'])))
        else:
            self.sku_seen.add(item['tienda'] + str(item['sku']))
            return item
        
class SaveInProductsDb(object):
    def process_item(self, item, spider):
        if item is not None:
            connection = MongoClient(MONGO_DB['HOST'], MONGO_DB['PORT'])
            db = connection[MONGO_DB['NAME']]
            db.authenticate(MONGO_DB['USER'], MONGO_DB['PASSWORD'])
            
            key = {
                'sku' : item['sku'],
                'tienda' : item['tienda']
            }
            
            data = {
                'sku' : item['sku'],
                'tienda' : item['tienda'],
                'marca' : item['marca'],
                'modelo' : item['modelo'],
                'descripcion' : item['descripcion'],
                'precio' : item['precio'],
                'categorias' : item['categorias'],
                'link' : item['link'],
                'actualizacion' : item['actualizacion'],
            }
            
            db.products.update(key, data, upsert=True)
        
        return item