# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import requests


class RequestHandlerBase(object):

    def get(self, url, params=None, headers=None):
        raise NotImplementedError

    def post(self, url, params=None, data=None, headers=None):
        raise NotImplementedError


class RequestHandler(RequestHandlerBase):

    @staticmethod
    def get_content(response):

        content_type = response.headers['content-type']

        if 'application/json' in content_type:
            return response.json()
        elif 'text/plain' in content_type:
            return response.text

        return None

    def request(self, method, url, **kwargs):
        r = requests.request(method, url, **kwargs)
        return self.get_content(r), r.status_code
