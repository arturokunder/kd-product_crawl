from scrapy.dupefilter import RFPDupeFilter

#from: http://stackoverflow.com/questions/12553117/how-to-filter-duplicate-requests-based-on-url-in-scrapy
class SeenUrlFilter(RFPDupeFilter):
    """A dupe filter that considers the URL"""

    def __init__(self, path=None):
        self.ids_seen = set()
        self.filtered = 0
        RFPDupeFilter.__init__(self, path)

    def __getUrlId(self, url):
        if 'falabella.com' in url or '/category/' in url:
            if '/product/' in url:
                return 'f' + url.split('/')[5]
        
        return None
    
    def request_seen(self, request):
        id = self.__getUrlId(request.url)
        if id is not None:
            if id in self.ids_seen:
                return True
            else:
                self.ids_seen.add(id)