import requests

from requests.auth import HTTPBasicAuth

from errors import SprintlyUnauthorizedException


class Api(object):
    def __init__(self, user, key):
        self._auth = HTTPBasicAuth(user, key)

    def _format_or_raise(self, response):
        # HTTP Unauthorized
        if response.status_code == 401:
            raise SprintlyUnauthorizedException(response.status_code,
                    response.reason)
        return response.json

    def _make_get_request(self, url):
        import sys
        response = requests.get(url, auth=self._auth, config={'verbose': sys.stderr})
        return self._format_or_raise(response)

    def _make_post_request(self, url, data):
        response = requests.post(url, data=data)
        return self._format_or_raise(response)

    def _make_delete_request(self, url):
        response = requests.delete(url)
        return self._format_or_raise(response)
