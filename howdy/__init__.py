# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

from howdy.cherry_picker import GoogleTextSearch, GoogleDetails, CherryPicker
from howdy.exceptions import AsyncLookupRequiredForRequest
from howdy.third_party_api.google import Google

class Howdy(object):
    """
    Search all api's for requested fields. Should give api's priority. Only search some api's if the data isn't found in others.
    This will allow the free/cheaper api's to be searched before the more expensive ones.

    """

    def __init__(self, storage=None, additional_cherry_pickers=None, request_handler=None):
        self.storage = storage
        self.request_handler = request_handler
        self.google = Google(storage=self.storage, request_handler=request_handler)
        self.google_text_search = GoogleTextSearch(self.google)
        self.google_details = GoogleDetails(self.google)
        self._additional_cherry_pickers = additional_cherry_pickers

    def __getattr__(self, item):
        if item == 'cherry_pickers':
            cherry_pickers = set()
            for cherry_picker in self._additional_cherry_pickers or ():
                cherry_pickers.add(cherry_picker(storage=self.storage, request_handler=self.request_handler))
            setattr(self, 'cherry_pickers', cherry_pickers)
            return cherry_pickers
        else:
            raise AttributeError(item)

    def say_howdy(self, caller_id, use_first_result=True, force=False):
        """
        caller_id is the number to search
        use_first_result is True if you only want to get all details for the first contact that matches the caller id.
        force is True if you want to not use previously found results

        Return:
            Results Found that match the caller id for the sources configured
            async_lookup_required will be True if the result is partially complete. That is some results could not be computed fast enough.
        """
        howdy_results = self.google_text_search(caller_id, force)
        async_lookup_required = False
        for howdy_model in howdy_results:
            self.google_details(howdy_model)  # Sets the domain which is needed for other sources
            for cherry_picker in self.cherry_pickers:
                if isinstance(cherry_picker, CherryPicker):
                    try:
                        cherry_picker(howdy_model)
                    except AsyncLookupRequiredForRequest:
                        async_lookup_required = True
            # Only use the first result found if multiple results are present and use_first_result is set to True
            if use_first_result:
                return howdy_model

        return howdy_results, async_lookup_required
