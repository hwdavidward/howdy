# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging
import unittest

from app.api.google.google import Google
from app.api.clearbit.clearbit_api import ClearbitAPI
from app.local_storage import DictionaryStorage

from app.howdy import Howdy, ClearbitCompanySource

"""
To run these tests create secret.py and define the a config that extends settings.py Config

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
        print 'Result is: %s' % results

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


class ClearbitTest(unittest.TestCase):

    def setUp(self):
        self.clearbitApi = ClearbitAPI()

    def testSearchDomain(self):
        domain = u'www.versature.com'
        result = self.clearbitApi.company_search(domain)
        self.assertIsNotNone(result)

class SayHowdyTest(unittest.TestCase):

    def setUp(self):
        self.howdy = Howdy(storage=DictionaryStorage(), domain_sources=[ClearbitCompanySource])

    def testSayHowdy(self):
        caller_id = '6132379329'
        result = self.howdy.say_howdy(caller_id)

        self.assertEqual(result.get('description', None), u'Canadian-based Hosted PBX provider, making business phone systems more awesome.')
        self.assertEqual(result.get('domain', None), u'www.versature.com')
        self.assertEqual(result.get('employees', None), 50)
        self.assertEqual(result.get('name', None), u'Versature')
        self.assertEqual(result.get('utc_offset', None), -240)
        self.assertEqual(result.get('website', None), u'http://www.versature.com/')
        self.assertEqual(result.get('linkedin', None), {u'handle': u'company/versature'})
        self.assertEqual(result.get('location', None), {u'lat': 45.457776, u'lng': -75.581728})
        self.assertEqual(result.get('facebook', None), {u'handle': u'versature', u'likes': None})
        self.assertIsNotNone(result.get('twitter', None))
        self.assertIsNotNone(result.get('logo', None))