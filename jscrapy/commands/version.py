import jjscrapy
from jjscrapy.commands import ScrapyCommand
from jjscrapy.utils.versions import jscrapy_components_versions


class Command(ScrapyCommand):

    default_settings = {'LOG_ENABLED': False,
                        'SPIDER_LOADER_WARN_ONLY': True}

    def syntax(self):
        return "[-v]"

    def short_desc(self):
        return "Print JSON Scrapy version"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_argument("--verbose", "-v", dest="verbose", action="store_true",
                            help="also display twisted/python/platform info (useful for bug reports)")

    def run(self, args, opts):
        if opts.verbose:
            versions = jscrapy_components_versions()
            width = max(len(n) for (n, _) in versions)
            for name, version in versions:
                print(f"{name:<{width}} : {version}")
        else:
            print(f"Scrapy {jjscrapy.__version__}")
