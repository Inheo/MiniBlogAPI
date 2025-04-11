from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session

from app.auth_service.schemas import Token
from app.db.database import get_db
from app.auth_service import models, schemas, security

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])

@router.post("/register", response_model=Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = security.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return security.generate_token(db_user)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return security.generate_token(user)

@router.post("/refresh", response_model=schemas.Token)
def refresh_jwt(user: models.User = Depends(security.get_current_auth_user_for_refresh)):
    return security.generate_token(user)