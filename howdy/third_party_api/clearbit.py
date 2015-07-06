# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import logging

from howdy_secrets import CLEARBIT_KEY
from howdy.third_party_api.base import RequestBase
from howdy.local_storage import memorized
from howdy.exceptions import AsyncLookupRequired

class Clearbit(RequestBase):
    """
    Clearbit API
    ====================

    https://person.clearbit.com/v1/people/email/alex@alexmaccaw.com

    """
    SOURCE_NAME = 'clearbit'
    COMPANY_SEARCH = 'company_search'
    COMPANY_CLEARBIT_URL = 'https://company.clearbit.com/v1/companies/'

    @memorized(SOURCE_NAME, COMPANY_SEARCH)
    def company_search(self, domain, force=False):
        url = self.COMPANY_CLEARBIT_URL + 'domain/' + domain
        headers = {'Authorization': 'Bearer ' + CLEARBIT_KEY}
        response, status_code = self.make_request('get', url, headers=headers)
        logging.debug("Google Text Search. Domain: %s, Response: %s, Status Code: %s", domain, response, status_code)
        if status_code == 202:
            raise AsyncLookupRequired(self.SOURCE_NAME, self.COMPANY_SEARCH)
        return response