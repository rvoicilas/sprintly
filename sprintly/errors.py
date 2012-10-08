class SprintlyException(Exception):
    pass


class SprintlyUnauthorizedException(SprintlyException):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

    def __str__(self):
        return '{0} - {1}'.format(self.status_code, self.reason)
