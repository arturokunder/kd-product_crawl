from scrapy.selector import HtmlXPathSelector 
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from crawler.items import newsItem 

class LaTerceraSpider(CrawlSpider):
    name = "latercera"
    allowed_domains = ["latercera.com"]
    start_urls = [
        "http://www.latercera.com/"
    ]
    rules = [Rule(SgmlLinkExtractor(allow=['/canal/'])),
             Rule(SgmlLinkExtractor(allow=['/noticia/']), 'parse_noticia')]
    

    def parse_noticia(self, response):
        sel = HtmlXPathSelector(response)
        item = newsItem()
        item['titular'] = sel.select('//*[@class="titularArticulo"]/text()').extract()
        item['bajada'] = sel.select('//*[@class="bajadaArt"]/text()').extract()
        item['noticia'] = sel.select('//*[@class="articleContent"]/p/text()').extract()
        item['link'] = response.url
        item['medio'] = 'La Tercera'
       
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
        return item