from unittest import TestCase
from urllib.parse import urlparse
import warnings

from jscrapy.http import Response, Request
from jscrapy.spiders import Spider
from jscrapy.spidermiddlewares.offsite import OffsiteMiddleware, URLWarning, PortWarning
from jscrapy.utils.test import get_crawler


class TestOffsiteMiddleware(TestCase):

    def setUp(self):
        crawler = get_crawler(Spider)
        self.spider = crawler._create_spider(**self._get_spiderargs())
        self.mw = OffsiteMiddleware.from_crawler(crawler)
        self.mw.spider_opened(self.spider)

    def _get_spiderargs(self):
        return dict(name='foo', allowed_domains=['jscrapytest.org', 'jscrapy.org', 'jscrapy.test.org'])

    def test_process_spider_output(self):
        res = Response('http://jscrapytest.org')

        onsite_reqs = [
            Request('http://jscrapytest.org/1'),
            Request('http://jscrapy.org/1'),
            Request('http://sub.jscrapy.org/1'),
            Request('http://offsite.tld/letmepass', dont_filter=True),
            Request('http://jscrapy.test.org/'),
            Request('http://jscrapy.test.org:8000/'),
        ]
        offsite_reqs = [
            Request('http://jscrapy2.org'),
            Request('http://offsite.tld/'),
            Request('http://offsite.tld/jscrapytest.org'),
            Request('http://offsite.tld/rogue.jscrapytest.org'),
            Request('http://rogue.jscrapytest.org.haha.com'),
            Request('http://roguejscrapytest.org'),
            Request('http://test.org/'),
            Request('http://notjscrapy.test.org/'),
        ]
        reqs = onsite_reqs + offsite_reqs

        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEqual(out, onsite_reqs)


class TestOffsiteMiddleware2(TestOffsiteMiddleware):

    def _get_spiderargs(self):
        return dict(name='foo', allowed_domains=None)

    def test_process_spider_output(self):
        res = Response('http://jscrapytest.org')
        reqs = [Request('http://a.com/b.html'), Request('http://b.com/1')]
        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEqual(out, reqs)


class TestOffsiteMiddleware3(TestOffsiteMiddleware2):

    def _get_spiderargs(self):
        return dict(name='foo')


class TestOffsiteMiddleware4(TestOffsiteMiddleware3):

    def _get_spiderargs(self):
        bad_hostname = urlparse('http:////jscrapytest.org').hostname
        return dict(name='foo', allowed_domains=['jscrapytest.org', None, bad_hostname])

    def test_process_spider_output(self):
        res = Response('http://jscrapytest.org')
        reqs = [Request('http://jscrapytest.org/1')]
        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEqual(out, reqs)


class TestOffsiteMiddleware5(TestOffsiteMiddleware4):

    def test_get_host_regex(self):
        self.spider.allowed_domains = ['http://jscrapytest.org', 'jscrapy.org', 'jscrapy.test.org']
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.mw.get_host_regex(self.spider)
            assert issubclass(w[-1].category, URLWarning)


class TestOffsiteMiddleware6(TestOffsiteMiddleware4):

    def test_get_host_regex(self):
        self.spider.allowed_domains = ['jscrapytest.org:8000', 'jscrapy.org', 'jscrapy.test.org']
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.mw.get_host_regex(self.spider)
            assert issubclass(w[-1].category, PortWarning)
