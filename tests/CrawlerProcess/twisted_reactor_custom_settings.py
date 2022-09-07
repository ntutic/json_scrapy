import jscrapy
from jscrapy.crawler import CrawlerProcess


class AsyncioReactorSpider(jscrapy.Spider):
    name = 'asyncio_reactor'
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }


process = CrawlerProcess()
process.crawl(AsyncioReactorSpider)
process.start()
