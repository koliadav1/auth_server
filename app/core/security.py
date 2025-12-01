from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.config import Config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        return result
    except Exception as e:
        return False

def get_password_hash(password: str) -> str:
    try:
        hashed = pwd_context.hash(password)
        return hashed
    except Exception as e:
        raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, Config.ACCESS_TOKEN_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, Config.REFRESH_TOKEN_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, is_refresh: bool = False) -> dict:
    try:
        secret_key = Config.REFRESH_TOKEN_SECRET_KEY if is_refresh else Config.ACCESS_TOKEN_SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=[Config.ALGORITHM])
        return payload
    except JWTError:
        return None