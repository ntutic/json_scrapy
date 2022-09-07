from unittest import TestCase

from jscrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from jscrapy.http import Request
from jscrapy.spiders import Spider
from jscrapy.utils.test import get_crawler
from jscrapy.utils.python import to_bytes


class TestDefaultHeadersMiddleware(TestCase):

    def get_defaults_spider_mw(self):
        crawler = get_crawler(Spider)
        spider = crawler._create_spider('foo')
        defaults = {
            to_bytes(k): [to_bytes(v)]
            for k, v in crawler.settings.get('DEFAULT_REQUEST_HEADERS').items()
        }
        return defaults, spider, DefaultHeadersMiddleware.from_crawler(crawler)

    def test_process_request(self):
        defaults, spider, mw = self.get_defaults_spider_mw()
        req = Request('http://www.jscrapytest.org')
        mw.process_request(req, spider)
        self.assertEqual(req.headers, defaults)

    def test_update_headers(self):
        defaults, spider, mw = self.get_defaults_spider_mw()
        headers = {'Accept-Language': ['es'], 'Test-Header': ['test']}
        bytes_headers = {b'Accept-Language': [b'es'], b'Test-Header': [b'test']}
        req = Request('http://www.jscrapytest.org', headers=headers)
        self.assertEqual(req.headers, bytes_headers)

        mw.process_request(req, spider)
        defaults.update(bytes_headers)
        self.assertEqual(req.headers, defaults)
