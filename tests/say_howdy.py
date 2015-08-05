# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging
import unittest

from howdy import Howdy
from howdy.local_storage import DictionaryStorage
from howdy.cherry_picker import ClearbitCompany
from howdy.exceptions import NoResultFound


"""
To run these tests create secret.py and define the a config that extends settings.py Config

i.e.

GOOGLE_PLACES_KEY = '123456789'

"""

logger = logging.getLogger(__name__)


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
