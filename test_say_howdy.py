# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging
import unittest

from howdy import Howdy
from howdy.local_storage import DictionaryStorage
from howdy.cherry_picker import ClearbitCompany
from howdy.exceptions import NoResultFound
from howdy.third_party_api.google import Google
from howdy.third_party_api.clearbit import Clearbit

"""
To run these tests create secret.py and define the a config that extends settings.py Config

i.e.

GOOGLE_PLACES_KEY = '123456789'

"""

logger = logging.getLogger(__name__)



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

    def test_search_caller_id_not_found(self):
        caller_id = 16133246100
        self.assertRaises(Exception, self.google.text_search, caller_id)

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

class FindSocialDataTest(unittest.TestCase):

    ############################################
    #### Find all Data for number/caller id ####
    ############################################

    def setUp(self):
        self.howdy = Howdy(storage=DictionaryStorage(), additional_cherry_pickers=[ClearbitCompany])

    def testSayHowdy(self):
        caller_id = '+16132379329'
        result = self.howdy.say_howdy(caller_id)

        self.assertEqual(result.get('description', None), u'Canadian-based Hosted PBX provider, making business phone systems more awesome.')
        self.assertEqual(result.get('formatted_address', None), u'5424 Canotek Road, Gloucester, ON K1J 1E9, Canada')
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

    def testSayHowdyNoResult(self):
        caller_id = '+16133246101'
        self.assertRaises(NoResultFound, self.howdy.say_howdy, caller_id)

    def testSayHowdyNoClearbitResult(self):
        caller_id = '+19053711777'
        result = self.howdy.say_howdy(caller_id)
        self.assertIsNone(result.get('description', None))
        self.assertEqual(result.get('formatted_address', None), u'7888 Oakwood Drive, Niagara Falls, ON L2E 6S5, Canada')
        self.assertEqual(result.get('domain', None), u'www.oktireniagara.com')
        self.assertIsNone(result.get('employees', None))
        self.assertEqual(result.get('name', None), u'OK Tire')
        self.assertEqual(result.get('utc_offset', None), -240)
        self.assertEqual(result.get('website', None), u'http://www.oktireniagara.com/')
        self.assertIsNone(result.get('linkedin', None))
        self.assertEqual(result.get('location', None), {u'lat': 43.061469, u'lng': -79.12092})
        self.assertIsNone(result.get('facebook', None))
        self.assertIsNone(result.get('twitter', None))
        self.assertIsNone(result.get('logo', None))


if __name__ == '__main__':
    unittest.main()