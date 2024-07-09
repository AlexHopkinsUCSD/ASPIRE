class BaseValidationError(Exception):
    def __init__(
        self, 
        message: str, 
        status_code: int, 
    ) -> None:
        
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message


class NonceValidationError(BaseValidationError):
    pass


class StateValidationError(BaseValidationError):
    pass


class TokenValidationError(BaseValidationError):
    pass