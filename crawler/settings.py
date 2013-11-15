# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {
                  #'crawler.pipelines.DropDuplicateItemPipeline' : 10,
                  'crawler.pipelines.SaveInProductsDb' : 20
                }

DOWNLOADER_MIDDLEWARES = {
    #'crawler.middlewares.RelCanonicalMiddleware': 10,
}

USER_AGENT = "Megustahotuiti/0.1"

#AUTOTHROTTLE_ENABLED = True

#CLOSESPIDER_PAGECOUNT = 50
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 1.8
DOWNLOAD_TIMEOUT = 40

DEPTH_LIMIT = 8

DUPEFILTER_CLASS = 'crawler.filters.SeenUrlFilter'

TELNETCONSOLE_PORT = [80, 5000]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'

