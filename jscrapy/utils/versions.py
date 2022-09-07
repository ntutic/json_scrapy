import platform
import sys

import cryptography
import cssselect
import lxml.etree
import parsel
import twisted
import w3lib

import jscrapy
from jscrapy.utils.ssl import get_openssl_version


def jscrapy_components_versions():
    lxml_version = ".".join(map(str, lxml.etree.LXML_VERSION))
    libxml2_version = ".".join(map(str, lxml.etree.LIBXML_VERSION))

    return [
        ("Scrapy", jscrapy.__version__),
        ("lxml", lxml_version),
        ("libxml2", libxml2_version),
        ("cssselect", cssselect.__version__),
        ("parsel", parsel.__version__),
        ("w3lib", w3lib.__version__),
        ("Twisted", twisted.version.short()),
        ("Python", sys.version.replace("\n", "- ")),
        ("pyOpenSSL", get_openssl_version()),
        ("cryptography", cryptography.__version__),
        ("Platform", platform.platform()),
    ]
