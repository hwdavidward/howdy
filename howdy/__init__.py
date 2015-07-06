# -*- coding: utf-8 -*-
__author__ = 'DavidWard'

from howdy.cherry_picker import GoogleTextSearch, GoogleDetails, CherryPicker
from howdy.exceptions import AsyncLookupRequired, PartialResultFound
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
        Search and get details about the provided caller_id from the initiated cherry pickers. If any request was unable
        to complete for any source a Partial Result Found Exception will be raised with the results that were computed.

        caller_id is the number to search
        use_first_result is True if you only want to get all details for the first contact that matches the caller id.
        force is True if you want to not use previously found results

        Return:
            Results Found that match the caller id for the sources configured
        """
        howdy_results = self.google_text_search(caller_id, force)
        async_lookup_required_exceptions = []
        for howdy_model in howdy_results:
            self.google_details(howdy_model)  # Sets the domain which is needed for other sources
            for cherry_picker in self.cherry_pickers:
                if isinstance(cherry_picker, CherryPicker):
                    try:
                        cherry_picker(howdy_model)
                    except AsyncLookupRequired as alr_except:
                        async_lookup_required_exceptions.append(alr_except)
            # Only use the first result found if multiple results are present and use_first_result is set to True
            if use_first_result:
                if not async_lookup_required_exceptions:
                    return howdy_model
                else:
                    raise PartialResultFound(howdy_model, async_lookup_required_exceptions)

        if async_lookup_required_exceptions:
            raise PartialResultFound(howdy_results, async_lookup_required_exceptions)

        return howdy_results
