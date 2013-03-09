class MockResponseUnauthorized(object):
    status_code = 401
    reason = 'UNAUTHORIZED'


class MockResponseValid(object):
    def __init__(self, data):
        self.status_code = 202
        self.json = data

class MockSprintlyResponse(object):
    def __init__(self, status_code, reason, json):
        self.status_code = status_code
        self.json = json
        self.reason = reason
