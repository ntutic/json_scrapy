import jscrapy
from jscrapy.crawler import CrawlerProcess


class SelectReactorSpider(jscrapy.Spider):
    name = 'epoll_reactor'


process = CrawlerProcess(settings={
    "TWISTED_REACTOR": "twisted.internet.selectreactor.SelectReactor",
})
process.crawl(SelectReactorSpider)
process.start()
