class SprintlyError(Exception):
    pass


class SprintlyUnauthorizedError(SprintlyError):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason
        self.message = '{0} - {1}'.format(self.status_code, self.reason)

    def __str__(self):
        return self.message
