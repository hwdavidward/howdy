# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

from urlparse import urlparse
from howdy.third_party_api.google.google import Google
from howdy.third_party_api.clearbit.clearbit_api import ClearbitAPI


class HowdyBaseSource(object):

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

class HowdySource(HowdyBaseSource):

    def __call__(self, howdy_model, force=False):
        raise NotImplementedError()

class GoogleTextSearchSource(HowdyBaseSource):

    def __init__(self, google=None, storage=None):
        if google:
            self.google = google
        else:
            self.google = Google(storage)

    def __call__(self, caller_id, force=False):
        """
        Parse the google text search results and set the correct attributes.
        """
        google_text_search_results = self.google.text_search(caller_id, force) or []
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

class GoogleDetailsSource(HowdyBaseSource):

    def __init__(self, google=None, storage=None):
        if google:
            self.google = google
        else:
            self.google = Google(storage)

    def __call__(self, howdy_model, force=False):
        """
        Parse the google text search results and set the correct attributes.
        """
        google_details_result = self.google.details(howdy_model['google_places_id'], force)
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

class ClearbitCompanySource(HowdySource):

    def __init__(self, clearbit=None, storage=None):
        if clearbit:
            self.clearbit = clearbit
        else:
            self.clearbit = ClearbitAPI(storage)

    def __call__(self, howdy_model, force=False):
        result = self.clearbit.company_search(howdy_model['domain'], force)
        self.parse_result(result, howdy_model)

    def parse_result(self, result, howdy_model):
        howdy_model['description'] = result.get('description', None)
        howdy_model['twitter'] = result.get('twitter', None)
        howdy_model['linkedin'] = result.get('linkedin', None)
        howdy_model['facebook'] = result.get('facebook', None)
        howdy_model['employees'] = result.get('employees', None)
        howdy_model['logo'] = result.get('logo', None)

class Howdy(object):
    """
    Search all api's for requested fields. Should give api's priority. Only search some api's if the data isn't found in others.
    This will allow the free/cheaper api's to be searched before the more expensive ones.

    """

    def __init__(self, storage=None, domain_sources=None, request_handler=None):
        self.storage = storage
        self.google = Google(storage=self.storage, request_handler=request_handler)
        self.google_text_search = GoogleTextSearchSource(self.google)
        self.google_details = GoogleDetailsSource(self.google)
        self.other_sources = set()
        self.initialize_sources(domain_sources)

    def initialize_sources(self, domain_sources):
        """
        Initialize Sources for lookup
        """
        for source in domain_sources:
            self.other_sources.add(source(storage=self.storage))

    def say_howdy(self, caller_id, use_first_result=True, force=False):
        """
        caller_id is the number to search
        fields is the values you are looking for
        """
        howdy_results = self.google_text_search(caller_id, force)

        for howdy_model in howdy_results:
            self.google_details(howdy_model)  # Sets the domain which is needed for other sources
            for source in self.other_sources:
                if isinstance(source, HowdySource):
                    source(howdy_model)

            # Only use the first result found if multiple results are present and use_first_result is set to True
            if use_first_result:
                return howdy_model

        return howdy_results
