# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging
from howdy.third_party_api.base import RequestBase
from howdy_secrets import GOOGLE_PLACES_KEY
from howdy.third_party_api.google.exceptions import GoogleError, NoGoogleResults
from howdy.local_storage import memorized

class Google(RequestBase):
    """
    Google Places API
    ====================


    Url Example: #https://maps.googleapis.com/maps/api/place/textsearch/json?key={key}&query={text query}

    -------------
    https://developers.google.com/places/webservice/intro

    """
    SOURCE_NAME = 'google'
    GOOGLE_PLACES_URL = 'https://maps.googleapis.com/maps/api/place/'

    TEXT_SEARCH = 'textsearch'
    DETAILS = 'details'

    def prepare_request(self, action):
        """
        Prepare the request for the provided action
        """
        url = self.GOOGLE_PLACES_URL + action + '/json'
        params = {'key': GOOGLE_PLACES_KEY}
        return url, params

    @memorized(SOURCE_NAME, TEXT_SEARCH)
    def text_search(self, text, force=False):
        url, params = self.prepare_request(self.TEXT_SEARCH)
        params['query'] = text
        response, status_code = self.make_request('get', url, params=params)
        logging.debug("Google Text Search. Text: %s, Response: %s, Status Code: %s", text, response, status_code)
        return response['results']

    @memorized(SOURCE_NAME, DETAILS)
    def details(self, place_id, force=False):
        url, params = self.prepare_request(self.DETAILS)
        params['placeid'] = place_id
        response, status_code = self.make_request('get', url, params=params)
        logging.debug("Google Details. Place Id: %s, Response: %s, Status Code: %s", place_id, response, status_code)
        return response['result']

    def validate_response(self, response, status_code):
        super(Google, self).validate_response(response, status_code)

        status = response.get('status', None)
        #if status == 'ZERO_RESULTS':
        #    raise NoGoogleResults()
        if status is None or status != 'OK':
            raise GoogleError('Invalid Status: {}'.format(status))