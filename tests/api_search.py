# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging
import unittest

from howdy.third_party_api.google import Google
from howdy.third_party_api.clearbit import Clearbit
from howdy.local_storage import DictionaryStorage

"""
To run these tests create howdy_secret.py and define the required key's.

i.e.

GOOGLE_PLACES_KEY = '123456789'
CLEARBIT_KEY = '123456789'

"""
logger = logging.getLogger(__name__)


class GooglePlacesTest(unittest.TestCase):

    def setUp(self):
        self.google = Google()

    ##############################
    #### GOOGLE PLACES SEARCH ####
    ##############################

    def test_search_caller_id(self):
        caller_id = 16132379329
        results = self.google.text_search(caller_id)
        self.assertIsNotNone(results)

    def test_place_id_request(self):
        place_id = u'ChIJL9V5DTEQzkwR2Iz9nMnPGkc'
        result = self.google.details(place_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.get('website', None), 'http://www.versature.com/')

class TestMemorizedResult(unittest.TestCase):

    def testGoogleDetails(self):
        google = Google(storage=DictionaryStorage())
        place_id = u'ChIJL9V5DTEQzkwR2Iz9nMnPGkc'
        details_response = google.details(place_id)
        self.assertIsNotNone(details_response)
        details_response_again = google.details(place_id)
        self.assertIsNotNone(details_response_again)
        #TODO test second response is cached result


class ClearbitDomainTest(unittest.TestCase):

    def testCompanyDomain(self):
        self.clearbitApi = Clearbit(storage=DictionaryStorage())
        domain = u'www.versature.com'
        result = self.clearbitApi.company_search(domain)
        self.assertIsNotNone(result)

