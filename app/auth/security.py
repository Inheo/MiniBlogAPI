from datetime import timedelta
from passlib.context import CryptContext
from app.config import settings
from .schemas import Token
from .models import User
from .dependencies import UserGetterFromToken, encode_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def generate_token(user: User) -> Token:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


def create_access_token(user: User):
    payload = {
        "sub": str(user.id),
        "id": user.id,
        "email": user.email,
    }

    return create_jwt(
        token_type=settings.token_config.ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def create_refresh_token(user: User):
    payload = {
        "sub": str(user.id),
    }
    return create_jwt(
        token_type=settings.token_config.REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    payload = {settings.token_config.TOKEN_TYPE_FIELD: token_type}
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

get_current_auth_user = UserGetterFromToken(settings.token_config.ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(settings.token_config.REFRESH_TOKEN_TYPE)