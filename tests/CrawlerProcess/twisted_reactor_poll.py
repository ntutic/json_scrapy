import jscrapy
from jscrapy.crawler import CrawlerProcess


class PollReactorSpider(jscrapy.Spider):
    name = 'poll_reactor'


process = CrawlerProcess(settings={
    "TWISTED_REACTOR": "twisted.internet.pollreactor.PollReactor",
})
process.crawl(PollReactorSpider)
process.start()
