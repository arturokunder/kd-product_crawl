from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from crawler.spiders.falabella_spider import FalabellaSpider
from crawler.spiders.paris_spider import ParisSpider
from scrapy.utils.project import get_project_settings

def setup_spider(spider):
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

print 'New crawl started'

log.start()

falabella = FalabellaSpider()
setup_spider(falabella)
paris = ParisSpider()
setup_spider(paris)

reactor.run()
