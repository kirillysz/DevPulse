from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from jwt import ExpiredSignatureError, InvalidTokenError
import jwt

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.TOKEN_EXPIRE))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        decoded = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded
    
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    
    except InvalidTokenError:
        raise ValueError("Invalid token")