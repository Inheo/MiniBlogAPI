from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.config import settings
from app.auth_service import models, schemas
from dependencies import UserGetterFromToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def generate_token(user: models.User) -> schemas.Token:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


def create_access_token(user: models.User):
    payload = {
        "sub": str(user.id),
        "id": user.id,
        "email": user.email,
    }

    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def create_refresh_token(user: models.User):
    payload = {
        "sub": str(user.id),
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    payload = {TOKEN_TYPE_FIELD: token_type}
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def encode_jwt(
    payload: dict,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
    algorithm: str = settings.ALGORITHM,
    secret_key: str = settings.SECRET_KEY,
) -> str:
    to_encode = payload.copy()
    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str,
    secret_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
) -> dict:
    decoded = jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )
    return decoded

def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {current_token_type!r} expected {token_type!r}"
        )


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)