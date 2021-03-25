from sanic_jwt.exceptions import SanicJWTException


class RefreshTokenFailed(SanicJWTException):
    status_code = 500

    def __init__(self, message="Refresh token failed.", **kwargs):
        super().__init__(message, **kwargs)


class CacheProcessFailed(SanicJWTException):
    status_code = 500

    def __init__(self, message="Cache process failed.", **kwargs):
        super().__init__(message, **kwargs)


class UnknownFailed(SanicJWTException):
    status_code = 500

    def __init__(self, message="Unknown failed.", **kwargs):
        super().__init__(message, **kwargs)
