# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

from urlparse import urlparse

from howdy.third_party_api.google import Google
from howdy.third_party_api.clearbit import Clearbit

class CherryPickerBase(object):

    def __init__(self, source=None, storage=None, request_handler=None):
        self.source = source
        self.storage = storage
        self.request_handler = request_handler

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class CherryPicker(CherryPickerBase):

    def __call__(self, howdy_model, force=False):
        raise NotImplementedError()

class GoogleTextSearch(CherryPickerBase):

    def __init__(self, source=None, storage=None, request_handler=None):
        super(GoogleTextSearch, self).__init__(source, storage, request_handler)
        if not source:
            self.source = Google(storage=storage, request_handler=request_handler)

    def __call__(self, caller_id, force=False):
        """
        Parse the google text search results and set the correct attributes.
        """
        google_text_search_results = self.source.text_search(caller_id, force) or []
        howdy_results = []

        for search_result in google_text_search_results:
            howdy_model = {}
            self.parse_result(search_result, howdy_model)
            howdy_results.append(howdy_model)
        return howdy_results

    def parse_result(self, result, howdy_model):
        howdy_model['google_places_id'] = result.get('place_id', None)
        howdy_model['name'] = result.get('name', None)
        geometry = result.get('geometry', None)
        howdy_model['location'] = geometry.get('location', None) if geometry else None

class GoogleDetails(CherryPickerBase):

    def __init__(self, source=None, storage=None, request_handler=None):
        super(GoogleDetails, self).__init__(source, storage, request_handler)
        if not source:
            self.source = Google(storage=storage, request_handler=request_handler)

    def __call__(self, howdy_model, force=False):
        """
        Parse the google text search results and set the correct attributes.
        """
        google_details_result = self.source.details(howdy_model['google_places_id'], force)
        self.parse_result(google_details_result, howdy_model)

    def parse_result(self, result, howdy_model):
        """

        """
        website = result.get('website', None)
        domain = None
        if website:
            domain = urlparse(website).hostname

        howdy_model['website'] = website
        howdy_model['domain'] = domain
        howdy_model['utc_offset'] = result.get('utc_offset', None)
        howdy_model['formatted_address'] = result.get('formatted_address', None)


class ClearbitCompany(CherryPicker):

    def __init__(self, source=None, storage=None, request_handler=None):
        super(ClearbitCompany, self).__init__(source, storage, request_handler)
        if not source:
            self.source = Clearbit(storage=storage, request_handler=request_handler)

    def __call__(self, howdy_model, force=False):
        result = self.source.company_search(howdy_model['domain'], force)
        self.parse_result(result, howdy_model)

    def parse_result(self, result, howdy_model):
        howdy_model['description'] = result.get('description', None)
        howdy_model['twitter'] = result.get('twitter', None)
        howdy_model['linkedin'] = result.get('linkedin', None)
        howdy_model['facebook'] = result.get('facebook', None)
        howdy_model['employees'] = result.get('employees', None)
        howdy_model['logo'] = result.get('logo', None)
