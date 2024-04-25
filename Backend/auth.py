"""Authentication of users using OAuth2."""

import os
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import User

CRYPT_SCHEMES = os.getenv("CRYPT_SCHEMES", "bcrypt").split()
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES", "60"))
SECRET_KEY = os.getenv("SECRET_KEY")

context = CryptContext(schemes=CRYPT_SCHEMES, deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(tags=["Authentication"])

def verify_password(plain_password: str, hashed_password: str):
    """Verify password with the hashed password."""
    return context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Return the hashed password."""
    return context.hash(password)

def get_user(username: str | None):
    """Return the user for given username."""
    user = db.session.query(User).filter(User.name == username).first()

    if user:
        return user
    return "User not found"      


def authenticate_user(username: str, password: str):
    """Authenticate the user using given credentials."""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user




