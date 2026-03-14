from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register_user(
    payload: schemas.UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = db.execute(
        select(models.User).where(
            or_(
                models.User.username == payload.username,
                models.User.email == payload.email,
            )
        )
    ).scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    user = models.User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=schemas.TokenOut,
    summary="Login and receive an access token",
)
def login_user(
    payload: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    user = db.execute(
        select(models.User).where(models.User.username == payload.username)
    ).scalars().first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(user.id, user.username)
    return {"access_token": token, "token_type": "bearer"}