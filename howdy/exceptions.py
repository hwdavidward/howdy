# -*- coding: utf-8 -*-
__author__ = 'DavidWard'


class HTTPError(Exception):
    pass

class NotFoundInStorage(Exception):
    pass

class ContentTypeNotSupported(Exception):
    pass

class AsyncLookupRequiredForRequest(Exception):

    def __init__(self, source, action):
        super(AsyncLookupRequiredForRequest, self).__init__(source, action)
        self.source = source
        self.action = action

class AsyncLookupRequired(Exception):

    def __init__(self, ):
        super(AsyncLookupRequired, self).__init__(source, action)
        self.source = source
        self.action = action