import json

import constants
from utils import format_datetime


class HTTPResponse:

    DEFAULT_REASON = {

    }

    def __init__(self,
                 body='',
                 content_type='text/html; chardet=utf-8;',
                 status=200,
                 headers=None
                 ):
        self.headers = headers or {}

        # Set default headers
        self.headers['Content-Type'] = content_type or 'text/html'
        self.status = status
        self.version = "1.1"
        self.upgrade = None # Websocket needed

    def set_cookie(self, key, value):
        self.headers['Set-Cookie'] = self.headers.get('Set-Cookie', '') + "%s=%s;" % (key, value)

    @property
    def status(self):
        return self._status

    @property
    def server_version(self):
        return "upyweb/%s" % constants.UPYWEB_VERSION

    @status.setter
    def status(self, value):
        if 100 <= value <= 999:
            self._status = value
        raise ValueError('Status code must be in range of 100 to 999')

    @property
    def reason(self):
        return self.DEFAULT_REASON.get(self.status, 'Unknown')

    @property
    def status_line(self):
        return 'HTTP/{self.version} {self.status} {self.reason}\r\n'.format(self)

    @property
    def content_type(self):
        return self.headers.get('Content-Type', '')

    @property
    def charset(self, default='UTF-8'):
        """ Return the charset specified in the content-type header (default: utf8). """
        if 'charset=' in self.content_type:
            return self.content_type.split('charset=')[-1].split(';')[0].strip()
        return default

    def _add_default_headers(self):
        # set the connection header
        connection = None
        if self.upgrade:
            connection = 'upgrade'
        elif not self.closing if self.keepalive is None else self.keepalive:
            if self.version == "1.0":
                connection = 'keep-alive'
        else:
            if self.version == "1.1":
                connection = 'close'

        if connection is not None:
            self.headers['Connection'] = connection

        if 'Date' not in self.headers:
            self.headers['Date'] = format_datetime(None)


        self.headers['Server'] = self.server_version

    def repr(self):
        pass



class JSONResponse(HTTPResponse):
    def __init__(self, data, **kwargs):
        if type(data) != dict:
            raise TypeError("Return data must be a dict")
        kwargs['content'] = json.dumps(data)
        
        super(JSONResponse, self).__init__(**kwargs)