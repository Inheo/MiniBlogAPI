from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.database import get_db
from app.auth_service import models
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


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
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_jwt(
    token: str,
    secret_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
) -> dict:
    return jwt.decode(token, secret_key, algorithms=[algorithm])


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(settings.token_config.TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
        )


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_jwt(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def get_user_by_token(payload: dict, db: Session) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
            self,
            payload: dict = Depends(get_current_token_payload),
            db: Session = Depends(get_db),
    ) -> models.User:
        validate_token_type(payload, self.token_type)
        return get_user_by_token(payload, db)