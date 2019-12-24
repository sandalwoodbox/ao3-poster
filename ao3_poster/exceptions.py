class LoginRequired(Exception):
    pass


class SessionExpired(Exception):
    pass


class UnexpectedError(Exception):
    pass


class ValidationError(Exception):
    def __init__(self, errors, *args, **kwargs):
        super(ValidationError, self).__init__(*args, **kwargs)
        self.errors = errors

    def __str__(self):
        return ', '.join(self.errors)
