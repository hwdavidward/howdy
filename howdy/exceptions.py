# -*- coding: utf-8 -*-
__author__ = 'DavidWard'


class HTTPError(Exception):
    pass

class NotFoundInStorage(Exception):
    pass

class ContentTypeNotSupported(Exception):
    pass

class AsyncLookupRequired(Exception):

    def __init__(self, source, action):
        super(AsyncLookupRequired, self).__init__(source, action)
        self.source = source
        self.action = action