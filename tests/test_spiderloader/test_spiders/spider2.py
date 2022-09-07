from jscrapy.spiders import Spider


class Spider2(Spider):
    name = "spider2"
    allowed_domains = ["jscrapy2.org", "jscrapy3.org"]
