import datetime

from scrapy.selector import HtmlXPathSelector 
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawler.items import productItem 

class ParisSpider(CrawlSpider):
    name = "paris"
    allowed_domains = ["www.paris.cl"]
    start_urls = [
        "http://www.paris.cl/static/"
        #'http://www.paris.cl/tienda/es/paris/frigobar-mabe-mac120b0'
        #'http://www.paris.cl/tienda/es/paris/linea-blanca/frigobar-y-cavas/frigobar-mabe-mac120b0'
    ]
    follow_canonical_links = False
    follow_canonical_links_url_exceptions = ["http://www.paris.cl/static/"]
    
    rules = [Rule(SgmlLinkExtractor(
                allow=[
                       r'/tienda/es/paris/search/',
                       r'/webapp/wcs/stores/servlet/SearchDisplay'
                ])),
             Rule(SgmlLinkExtractor(
                allow=[
                       r'/tienda/es/paris/[-\w+]+$',
                       r'/tienda/es/paris/[-\w+]+#[\.\w+]+$',
                       r'/tienda/es/paris/[-\w+]+/[-\w+]+/[-\w+]+$',
                       r'/tienda/es/paris/[-\w+]+/[-\w+]+/[-\w+]+#[\.\w+]+$',
                       r'/tienda/ProductDisplay'
                ]), 
                'parse_producto')
            ]
    

    def parse_producto(self, response):
        sel = HtmlXPathSelector(response)
        item = productItem()
        
        sku = sel.select('//span[@class="sku"]/text()').extract()
        if(len(sku) == 0):
            return None
        else:
            item['sku'] = get_item(sku).replace('SKU: ', '')
        
        marca = ''
        ficha_tecnica = sel.select('//div[@class="datasheet"]/table//tr/td/text()').extract()
        if len(ficha_tecnica) >= 2:
            for idx, i in enumerate(ficha_tecnica):
                if i.lower() == 'marca' and len(ficha_tecnica) >= idx+1:
                    marca = ficha_tecnica[idx+1]
                    break
        
        item['marca'] = marca
        item['modelo'] = clean_item(get_item(sel.select('//*[@id="catalog_link"]/text()').extract())).replace(' ' + marca, '')
        
        item['descripcion'] = clean_item(u' '.join(sel.select('//div[@class="description" or @class="datasheet"]/*').extract()))
        
        item['categorias'] = sel.select('//div[@id="WC_BreadCrumbTrailDisplay_div_1"]/a/text()').extract()
        
        item['tienda'] = 'Paris'
        item['link'] = response.url
        item['actualizacion'] = datetime.datetime.now()
        
        precio = {}
        internet = sel.select('//*[@class="price offerPrice bold"]/text()').extract()
        if len(internet) > 1:
            internet = internet[0]
            
        precio['internet'] = get_number(clean_item(get_item(internet)))

        hayoferta = sel.select('substring-after(//span[@class="sub-price bold"]/text(), "$")').extract()
        
        if len(hayoferta) > 0 and len(hayoferta[0]) > 0:
            precio['oferta'] = precio['internet']
            precio['internet'] = get_number(clean_item(get_item(hayoferta)))
            
        item['precio'] = precio
        
        return item
    
def get_number(result):
    try:
        result = result.replace(u'.', u'').replace(u'$', u'')
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