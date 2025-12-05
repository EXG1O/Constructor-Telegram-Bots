from jwt import InvalidTokenError


class InvalidTokenTypeError(InvalidTokenError):
    pass


class InvalidTokenSubjectError(InvalidTokenError):
    pass


class InvalidTokenRefreshJTIError(InvalidTokenError):
    pass
