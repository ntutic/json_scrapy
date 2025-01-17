from w3lib.url import parse_data_uri

from jscrapy.http import TextResponse
from jscrapy.responsetypes import responsetypes
from jscrapy.utils.decorators import defers


class DataURIDownloadHandler:
    lazy = False

    @defers
    def download_request(self, request, spider):
        uri = parse_data_uri(request.url)
        respcls = responsetypes.from_mimetype(uri.media_type)

        resp_kwargs = {}
        if (issubclass(respcls, TextResponse)
                and uri.media_type.split('/')[0] == 'text'):
            charset = uri.media_type_parameters.get('charset')
            resp_kwargs['encoding'] = charset

        return respcls(url=request.url, body=uri.data, **resp_kwargs)
