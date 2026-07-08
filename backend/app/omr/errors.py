class OMRError(Exception):
    status_code = 422

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class OMRValidationError(OMRError):
    status_code = 400


class OMRConfigurationError(OMRError):
    status_code = 503


class OMRTimeoutError(OMRError):
    status_code = 504


class OMREngineError(OMRError):
    status_code = 422
