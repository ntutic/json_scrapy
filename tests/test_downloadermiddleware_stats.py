import warnings
from itertools import product
from unittest import TestCase

from jscrapy.downloadermiddlewares.stats import DownloaderStats
from jscrapy.exceptions import ScrapyDeprecationWarning
from jscrapy.http import Request, Response
from jscrapy.spiders import Spider
from jscrapy.utils.response import response_httprepr
from jscrapy.utils.test import get_crawler


class MyException(Exception):
    pass


class TestDownloaderStats(TestCase):

    def setUp(self):
        self.crawler = get_crawler(Spider)
        self.spider = self.crawler._create_spider('jscrapytest.org')
        self.mw = DownloaderStats(self.crawler.stats)

        self.crawler.stats.open_spider(self.spider)

        self.req = Request('http://jscrapytest.org')
        self.res = Response('jscrapytest.org', status=400)

    def assertStatsEqual(self, key, value):
        self.assertEqual(
            self.crawler.stats.get_value(key, spider=self.spider),
            value,
            str(self.crawler.stats.get_stats(self.spider))
        )

    def test_process_request(self):
        self.mw.process_request(self.req, self.spider)
        self.assertStatsEqual('downloader/request_count', 1)

    def test_process_response(self):
        self.mw.process_response(self.req, self.res, self.spider)
        self.assertStatsEqual('downloader/response_count', 1)

    def test_response_len(self):
        body = (b'', b'not_empty')  # empty/notempty body
        headers = ({}, {'lang': 'en'}, {'lang': 'en', 'User-Agent': 'jscrapy'})  # 0 headers, 1h and 2h
        test_responses = [  # form test responses with all combinations of body/headers
            Response(
                url='jscrapytest.org',
                status=200,
                body=r[0],
                headers=r[1]
            )
            for r in product(body, headers)
        ]
        for test_response in test_responses:
            self.crawler.stats.set_value('downloader/response_bytes', 0)
            self.mw.process_response(self.req, test_response, self.spider)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", ScrapyDeprecationWarning)
                resp_size = len(response_httprepr(test_response))
            self.assertStatsEqual('downloader/response_bytes', resp_size)

    def test_process_exception(self):
        self.mw.process_exception(self.req, MyException(), self.spider)
        self.assertStatsEqual('downloader/exception_count', 1)
        self.assertStatsEqual(
            'downloader/exception_type_count/tests.test_downloadermiddleware_stats.MyException',
            1
        )

    def tearDown(self):
        self.crawler.stats.close_spider(self.spider, '')
