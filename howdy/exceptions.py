# -*- coding: utf-8 -*-
__author__ = 'DavidWard'


class HTTPError(Exception):

    def __init__(self, msg, status_code):
        super(HTTPError, self).__init__(msg)
        self.status_code = status_code

class NotFoundInStorage(Exception):
    pass

class ContentTypeNotSupported(Exception):
    pass

class AsyncLookupRequired(Exception):

    def __init__(self, source, action):
        super(AsyncLookupRequired, self).__init__(source, action)
        self.source = source
        self.action = action


class PartialResultFound(Exception):

    def __init__(self, result, source_exceptions):
        self.result = result
        self.source_exceptions = source_exceptions
        super(PartialResultFound, self).__init__(result, source_exceptions)

class NoResultFound(Exception):
    pass