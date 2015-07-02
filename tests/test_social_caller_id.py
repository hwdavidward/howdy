# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging
import unittest

#from secret import GOOGLE_PLACES_KEY

"""
To run these tests create secret.py and define the a config that extends settings.py Config

i.e.

GOOGLE_PLACES_KEY = '123456789'

"""

logger = logging.getLogger(__name__)


class FindSocialDataTest(unittest.TestCase):

    ##################################
    #### Find all Data for number ####
    ##################################

    def test_find_versature_social_data(self):
        caller_id = 6132379329
        # TODO

    def test_find_versature_toll_free_social_data(self):
        caller_id = None
        # TODO
