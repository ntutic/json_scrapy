import jscrapy
from jscrapy.crawler import CrawlerProcess


class AsyncioReactorSpider(jscrapy.Spider):
    name = 'asyncio_reactor'


process = CrawlerProcess(settings={
    "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
})
process.crawl(AsyncioReactorSpider)
process.start()
