# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging
from functools import wraps
from howdy.exceptions import NotFoundInStorage

class Storage(object):

    def get(self, api_name, action, *args, **kwargs):
        raise NotImplementedError()

    def set(self, api_name, action, value):
        raise NotImplementedError()

class DictionaryStorage(Storage):

    def __init__(self):
        self.cached = {}

    def get(self, api_name, action, *args, **kwargs):
        try:
            return self.cached[api_name+action+str(args)+str(kwargs)]
        except KeyError:
            raise NotFoundInStorage()

    def set(self, api_name, action, value, *args, **kwargs):
        self.cached[api_name+action+str(args)+str(kwargs)] = value

def memorized(api_name, action):
    def mem(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            self = args[0]
            storage = self.storage
            args = args[1:]
            force = kwargs.pop('force', False)
            try:
                if force is True or storage is None:
                    raise NotFoundInStorage()
                result = storage.get(api_name, action, *args, **kwargs)
                logging.debug('Request was memorized. Result: %s', result)
            except NotFoundInStorage:
                result = fun(self, *args, **kwargs)
                if storage is not None:
                    storage.set(api_name, action, result, *args, **kwargs)
            return result
        return wrapper
    return mem
