import jscrapy
from jscrapy.crawler import CrawlerProcess


class SelectReactorSpider(jscrapy.Spider):
    name = 'select_reactor'
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.selectreactor.SelectReactor",
    }


class AsyncioReactorSpider(jscrapy.Spider):
    name = 'asyncio_reactor'
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }


process = CrawlerProcess()
process.crawl(SelectReactorSpider)
process.crawl(AsyncioReactorSpider)
process.start()
