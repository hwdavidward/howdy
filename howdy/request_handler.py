# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import requests
from howdy.exceptions import ContentTypeNotSupported

class RequestHandlerBase(object):

    def request(self, method, url, **kwargs):
        raise NotImplementedError


class RequestHandler(RequestHandlerBase):

    @staticmethod
    def get_content(response):

        content_type = response.headers['content-type']

        if 'application/json' in content_type:
            return response.json()
        elif 'text/plain' in content_type:
            return response.text
        else:
            raise ContentTypeNotSupported('Content Type: %s is not supported' % content_type)

    def request(self, method, url, **kwargs):
        r = requests.request(method, url, **kwargs)
        return self.get_content(r), r.status_code
