# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

from howdy.request_handler import RequestHandler, RequestHandlerBase
from howdy.exceptions import HTTPError
from howdy.local_storage import Storage

class RequestBase(object):

    def __init__(self, storage=None, **kwargs):
        self.storage = storage
        self.request_handler = kwargs.pop('request_handler', None) or RequestHandler()
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r', kwargs)

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        if value is not None and not isinstance(value, Storage):
            raise TypeError('Invalid Storage Service provided. Must be subclass of Storage')
        self._storage = value

    @property
    def request_handler(self):
        return self._request_handler

    @request_handler.setter
    def request_handler(self, value):
        if not isinstance(value, RequestHandlerBase):
            raise TypeError('Invalid Request Handler Provided. Must be subclass of RequestHandlerBase')
        self._request_handler = value

    def make_request(self, method, url, data=None, params=None, headers=None, timeout=60):
        response, status_code = self.request_handler.request(method, url, data=data, params=params, headers=headers, timeout=timeout)
        self.validate_response(response, status_code)
        return response, status_code

    def validate_response(self, response, status_code):
        """
        Validate the provided response content and status code.
        """

        http_error_msg = ''

        if 400 <= status_code < 500:
            http_error_msg = '%s Client Error' % status_code

        elif 500 <= status_code < 600:
            http_error_msg = '%s Server Error' % status_code

        if http_error_msg:
            raise HTTPError(http_error_msg, status_code)
