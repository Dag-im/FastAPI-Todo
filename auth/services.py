from sqlalchemy.orm import Session
from auth.schema import Token
from auth.utils import verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.database import get_db
from users.models import User as UserItem
from fastapi import Depends, HTTPException, status
from users.models import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    data = decode_token(token)
    if not data:
        return None
    user = db.query(UserItem).filter(UserItem.email == data.email).first()
    return user

def get_current_admin(current_user: UserItem = Depends(get_current_user)):
    if not current_user or current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def validate_user(db: Session, email: str, password: str):
    user = db.query(UserItem).filter(UserItem.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, form_data: OAuth2PasswordRequestForm):
    user = validate_user(db, form_data.username, form_data.password)
    if not user:
        return {"status_code": 401, "detail": "Incorrect email or password"}
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}
