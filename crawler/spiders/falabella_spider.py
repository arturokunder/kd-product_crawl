import datetime
import re

from scrapy.http import Request
from scrapy.selector import Selector 
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawler.items import productItem 

class FalabellaSpider(CrawlSpider):
    name = "falabella"
    allowed_domains = ["www.falabella.com"]
    start_urls = [
        #"http://www.falabella.com/falabella-cl/"
        'http://www.falabella.com/falabella-cl/category/cat70043/LED'
    ]
    #deny secure.falabella.com
    rules = [Rule(SgmlLinkExtractor(allow=['/falabella-cl/category/'], 
                                    deny=['/falabella-cl/browse/', '/falabella-cl/myaccount/', '/static/site/']),
                  callback='parse_categoria', follow=True),
             Rule(SgmlLinkExtractor(allow=['/falabella-cl/product/']), 'parse_producto')]
    
    def parse_categoria(self, response):
        sel = Selector(response)
        #hrefs = sel.xpath('//div[@id="paginador"]/a[matches(@href, "javascript:goToPage\(\d+\)")]/@href')
        hrefs = sel.xpath('//div[@id="paginador"]/a/@href').extract()
        regex = re.compile(r"javascript:goToPage\(\d+\);")
        for h in hrefs:
            if re.match('javascript:goToPage\(\d+\);$', h):
                page = re.search('\d+', h).group(0)
                url = 'http://www.falabella.com/' + sel.xpath('//form[@id="facetsForm"]/@action').extract()[0] + '?'
                
                url = url + '_dyncharset=' + sel.xpath('//form[@id="facetsForm"]//input[@name="_dyncharset"]/@value').extract()[0] + '&'
                url = url + 'requestChainToken=' + sel.xpath('//form[@id="facetsForm"]//input[@name="requestChainToken"]/@value').extract()[0] + '&'
                url = url + 'goToPage=' + page + '&'
                url = url + 'pageSize=' + sel.xpath('//form[@id="facetsForm"]//input[@name="pageSize"]/@value').extract()[0] + '&'
                url = url + 'priceFlag=' + sel.xpath('//form[@id="facetsForm"]//input[@name="priceFlag"]/@value').extract()[0] + '&'
                url = url + 'categoryId=' + sel.xpath('//form[@id="facetsForm"]//input[@name="categoryId"]/@value').extract()[0] + '&'
                url = url + 'docSort=' + sel.xpath('//form[@id="facetsForm"]//input[@name="docSort"]/@value').extract()[0] + '&'
                url = url + 'docSortProp=' + sel.xpath('//form[@id="facetsForm"]//input[@name="docSortProp"]/@value').extract()[0] + '&'
                url = url + 'docSortOrder=' + sel.xpath('//form[@id="facetsForm"]//input[@name="docSortOrder"]/@value').extract()[0] + '&'
                url = url + 'onlineStoreFilter=' + sel.xpath('//form[@id="facetsForm"]//input[@name="onlineStoreFilter"]/@value').extract()[0] + '&'
                url = url + 'userSelectedFormat=' + sel.xpath('//form[@id="facetsForm"]//input[@name="userSelectedFormat"]/@value').extract()[0] + '&'
                url = url + 'trail=' + sel.xpath('//form[@id="facetsForm"]//input[@name="trail"]/@value').extract()[0] + '&'
                url = url + 'navAction=' + sel.xpath('//form[@id="facetsForm"]//input[@name="navAction"]/@value').extract()[0] + '&'
                url = url + 'searchCategory=' + sel.xpath('//form[@id="facetsForm"]//input[@name="searchCategory"]/@value').extract()[0] + '&'
                url = url + 'question=' + sel.xpath('//form[@id="facetsForm"]//input[@name="question"]/@value').extract()[0] + '&'
                url = url + 'searchColorGroupFacet=' + sel.xpath('//form[@id="facetsForm"]//input[@name="searchColorGroupFacet"]/@value').extract()[0] + '&'
                url = url + 'qfh_s_s=' + sel.xpath('//form[@id="facetsForm"]//input[@name="qfh_s_s"]/@value').extract()[0] + '&'
                url = url + '_D:qfh_s_s=' + sel.xpath('//form[@id="facetsForm"]//input[@name="_D:qfh_s_s"]/@value').extract()[0] + '&'
                url = url + 'qfh_ft=' + sel.xpath('//form[@id="facetsForm"]//input[@name="qfh_ft"]/@value').extract()[0] + '&'
                url = url + '_D:qfh_ft=' + sel.xpath('//form[@id="facetsForm"]//input[@name="_D:qfh_ft"]/@value').extract()[0] + '&'
                url = url + '_DARGS=' + sel.xpath('//form[@id="facetsForm"]//input[@name="_DARGS"]/@value').extract()[0]
                yield Request(url)
    
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