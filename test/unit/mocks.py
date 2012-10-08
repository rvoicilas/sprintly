class MockResponseUnauthorized(object):
    status_code = 401
    reason = 'UNAUTHORIZED'


class MockResponseValid(object):
    def __init__(self, data):
        self.status_code = 202
        self.json = data
