import datetime

from scrapy.selector import Selector 
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawler.items import productItem 

class FalabellaSpider(CrawlSpider):
    name = "falabella"
    allowed_domains = ["www.falabella.com"]
    start_urls = [
        "http://www.falabella.com/falabella-cl/"
    ]
    #deny secure.falabella.com
    rules = [Rule(SgmlLinkExtractor(allow=['/falabella-cl/category/'], 
                                    deny=['/falabella-cl/browse/', '/falabella-cl/myaccount/', '/static/site/'])),
             Rule(SgmlLinkExtractor(allow=['/falabella-cl/product/']), 'parse_producto')]
    

    def parse_producto(self, response):
        sel = Selector(response)
        item = productItem()
        
        item['marca'] = clean_item(get_item(sel.xpath('//div[@class="detalle"]/div[@class="marca"]/text()').extract()))
        item['modelo'] = clean_item(get_item(sel.xpath('//*[@id="productDecription"]/text()').extract()))
        item['descripcion'] = u' '.join(sel.xpath('//div[@id="contenidoDescripcionPP"]/*').extract())
        
        item['categorias'] = sel.xpath('//div[@id="ruta"]/a[not(contains(., "Falabella.com"))]/text()').extract()
       
        item['tienda'] = 'Falabella'
        item['link'] = response.url
        
        item['sku'] = get_number(response.url.split('/')[5])
        
        item['actualizacion'] = datetime.datetime.now()
        
        internet = sel.xpath('//div[@id="preciosPP"]//div[@class="precio1"]/text()').extract()
       
        if len(internet) == 2:
            internet = [internet[1]]
            
        precio = {
                'normal' : get_number(clean_item(get_item(sel.xpath('substring-after(//div[@id="preciosPP"]//div[@class="precio2"]/text(), "$")').extract()))),
                'internet' : get_number(clean_item(get_item(internet))),
                  }
        item['precio'] = precio
        
        return item
    
def get_number(result):
    try:
        result = result.replace(u'.', u'')
        return int(result)
    except:
        return result

def clean_item(result):
    try:
        return result.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\t', u'').replace(u'\r', u'')
    except:
        return result

def get_item(xpath_result):
    if len(xpath_result) == 1:
        return xpath_result[0]
    return xpath_result