import jscrapy
from jscrapy.crawler import CrawlerProcess


class NoRequestsSpider(jscrapy.Spider):
    name = 'no_request'

    def start_requests(self):
        return []


process = CrawlerProcess(settings={
    "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
})
process.crawl(NoRequestsSpider)
process.start()
