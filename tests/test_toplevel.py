from unittest import TestCase

import jscrapy


class ToplevelTestCase(TestCase):

    def test_version(self):
        self.assertIs(type(jscrapy.__version__), str)

    def test_version_info(self):
        self.assertIs(type(jscrapy.version_info), tuple)

    def test_request_shortcut(self):
        from jscrapy.http import Request, FormRequest
        self.assertIs(jscrapy.Request, Request)
        self.assertIs(jscrapy.FormRequest, FormRequest)

    def test_spider_shortcut(self):
        from jscrapy.spiders import Spider
        self.assertIs(jscrapy.Spider, Spider)

    def test_selector_shortcut(self):
        from jscrapy.selector import Selector
        self.assertIs(jscrapy.Selector, Selector)

    def test_item_shortcut(self):
        from jscrapy.item import Item, Field
        self.assertIs(jscrapy.Item, Item)
        self.assertIs(jscrapy.Field, Field)
