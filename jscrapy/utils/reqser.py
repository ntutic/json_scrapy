import warnings
from typing import Optional

import jscrapy
from jscrapy.exceptions import ScrapyDeprecationWarning
from jscrapy.utils.request import request_from_dict as _from_dict


warnings.warn(
    ("Module jscrapy.utils.reqser is deprecated, please use request.to_dict method"
     " and/or jscrapy.utils.request.request_from_dict instead"),
    category=ScrapyDeprecationWarning,
    stacklevel=2,
)


def request_to_dict(request: "jscrapy.Request", spider: Optional["jscrapy.Spider"] = None) -> dict:
    return request.to_dict(spider=spider)


def request_from_dict(d: dict, spider: Optional["jscrapy.Spider"] = None) -> "jscrapy.Request":
    return _from_dict(d, spider=spider)
