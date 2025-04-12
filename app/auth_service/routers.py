from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.auth_service import schemas, models
from app.db.database import get_db
from app.auth_service.security import (
    hash_password,
    verify_password,
    generate_token,
    get_current_auth_user_for_refresh,
)
from app.auth_service.dependencies import get_current_token_payload

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    user = models.User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/token", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return generate_token(user)


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    current_user: models.User = Depends(get_current_auth_user_for_refresh)
):
    return generate_token(current_user)