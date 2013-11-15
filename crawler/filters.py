import re

from scrapy.dupefilter import RFPDupeFilter
from w3lib.url import url_query_parameter 

#from: http://stackoverflow.com/questions/12553117/how-to-filter-duplicate-requests-based-on-url-in-scrapy
class SeenUrlFilter(RFPDupeFilter):
    """A dupe filter that considers the URL"""

    def __init__(self, path=None):
        self.ids_seen = set()
        self.filtered = 0
        RFPDupeFilter.__init__(self, path)

    def __getUrlId(self, url):
        if 'falabella.com' in url:
            if '/product/' in url or '/category/' in url:
                return 'f' + url.split('/')[5]
        
        if 'paris.cl' in url:
            if '/tienda/es/paris' in url:
                return 'p' + url.split('/')[::-1][0].split('#')[0]
            elif re.search(r'/webapp/wcs/stores/servlet/SearchDisplay\?(?=.*categoryId=\w+)(?=.*pageSize=\d+)', url):
                return 'p' + url_query_parameter(url, 'categoryId', keep_blank_values=True)
        
        return None
    
    def request_seen(self, request):
        id = self.__getUrlId(request.url)
        if id is not None:
            if id in self.ids_seen:
                return True
            else:
                self.ids_seen.add(id)