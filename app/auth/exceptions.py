from fastapi import HTTPException, status
from jose import JWTError


class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )


class InvalidUserCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


class InvalidTokenTypeException(HTTPException):
    def __init__(self, current_token_type: str, token_type: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
        )


class InvalidTokenException(HTTPException):
    def __init__(self, jwt_error: JWTError):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token {jwt_error}",
            headers={"WWW-Authenticate": "Bearer"}
        )


class InvalidCredentialsByTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )