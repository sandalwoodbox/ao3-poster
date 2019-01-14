class LoginRequired(Exception):
    pass


class SessionExpired(Exception):
    pass


class ValidationError(Exception):
    def __init__(self, errors, *args, **kwargs):
        super(ValidationError, self).__init__(*args, **kwargs)
        self.errors = errors
