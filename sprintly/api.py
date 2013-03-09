import requests
import sys

from requests.auth import HTTPBasicAuth

from errors import SprintlyUnauthorizedError


class Api(object):
    def __init__(self, user, key, debug=False):
        self._session = requests.session(auth=HTTPBasicAuth(user, key))
        if debug:
            self.session.config.update({'verbose': sys.stderr})

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    def _format_or_raise(self, response):
        # HTTP Unauthorized or HTTP Forbidden
        if response.status_code in (401, 403):
            raise SprintlyUnauthorizedError(
                    response.status_code,
                    response.reason)
        return response.json

    def _make_get_request(self, url, params=None):
        response = self._session.get(url, params=params)
        return self._format_or_raise(response)

    def _make_post_request(self, url, data):
        response = self._session.post(url, data=data)
        return self._format_or_raise(response)

    def _make_delete_request(self, url):
        response = self._session.delete(url)
        return self._format_or_raise(response)
