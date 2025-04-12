from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security import validate_token_type, oauth2_scheme, decode_jwt
from app.db.database import get_db
from jose import JWTError
from fastapi import status
from app.auth_service import models


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