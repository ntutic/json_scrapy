from w3lib.url import file_uri_to_path

from jscrapy.responsetypes import responsetypes
from jscrapy.utils.decorators import defers


class FileDownloadHandler:
    lazy = False

    @defers
    def download_request(self, request, spider):
        filepath = file_uri_to_path(request.url)
        with open(filepath, 'rb') as fo:
            body = fo.read()
        respcls = responsetypes.from_args(filename=filepath, body=body)
        return respcls(url=request.url, body=body)
