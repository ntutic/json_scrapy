from unittest import TestCase

from testfixtures import LogCapture

from jscrapy.spidermiddlewares.urllength import UrlLengthMiddleware
from jscrapy.http import Response, Request
from jscrapy.spiders import Spider
from jscrapy.utils.test import get_crawler
from jscrapy.settings import Settings


class TestUrlLengthMiddleware(TestCase):

    def setUp(self):
        self.maxlength = 25
        settings = Settings({'URLLENGTH_LIMIT': self.maxlength})

        crawler = get_crawler(Spider)
        self.spider = crawler._create_spider('foo')
        self.stats = crawler.stats
        self.mw = UrlLengthMiddleware.from_settings(settings)

        self.response = Response('http://jscrapytest.org')
        self.short_url_req = Request('http://jscrapytest.org/')
        self.long_url_req = Request('http://jscrapytest.org/this_is_a_long_url')
        self.reqs = [self.short_url_req, self.long_url_req]

    def process_spider_output(self):
        return list(self.mw.process_spider_output(self.response, self.reqs, self.spider))

    def test_middleware_works(self):
        self.assertEqual(self.process_spider_output(), [self.short_url_req])

    def test_logging(self):
        with LogCapture() as log:
            self.process_spider_output()

        ric = self.stats.get_value('urllength/request_ignored_count', spider=self.spider)
        self.assertEqual(ric, 1)

        self.assertIn(f'Ignoring link (url length > {self.maxlength})', str(log))
