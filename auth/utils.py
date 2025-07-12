from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from auth.schema import TokenData
from core.config import Settings
from fastapi import HTTPException

# Hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    # Add exp, then encode
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            return None
        return TokenData(email=email, role=role)
    except JWTError:
        return None
def create_password_reset_token(email: str) -> str:
    data = {"sub": email, "scope": "pwd-reset"}
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)

def verify_password_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        if payload.get("scope") != "pwd-reset":
            raise JWTError("Invalid scope")
        return payload.get("sub")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired reset token") from e
