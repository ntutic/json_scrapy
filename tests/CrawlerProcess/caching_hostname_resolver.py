import sys

import jscrapy
from jscrapy.crawler import CrawlerProcess


class CachingHostnameResolverSpider(jscrapy.Spider):
    """
    Finishes in a finite amount of time (does not hang indefinitely in the DNS resolution)
    """
    name = "caching_hostname_resolver_spider"

    def start_requests(self):
        yield jscrapy.Request(self.url)

    def parse(self, response):
        for _ in range(10):
            yield jscrapy.Request(response.url, dont_filter=True, callback=self.ignore_response)

    def ignore_response(self, response):
        self.logger.info(repr(response.ip_address))


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "RETRY_ENABLED": False,
        "DNS_RESOLVER": "jscrapy.resolver.CachingHostnameResolver",
    })
    process.crawl(CachingHostnameResolverSpider, url=sys.argv[1])
    process.start()
