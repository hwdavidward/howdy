# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

import clearbit

from howdy.third_party_api.base import Base
from howdy.local_storage import memorized
from secret import CLEARBIT_KEY

clearbit.key = CLEARBIT_KEY


class ClearbitAPI(Base):
    """
    Clearbit API
    ====================

    """

    @memorized('clearbit', 'company_search')
    def company_search(self, domain, force=False):
        return dict(clearbit.Company.find(domain=domain))