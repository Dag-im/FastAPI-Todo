from sqlalchemy.orm import Session
from users.models import User, Role
from users.schema import UserCreate, UserUpdate
from auth.utils import get_password_hash, create_password_reset_token, verify_password_reset_token
from core.config import Settings
from fastapi import HTTPException, status

def create_user(db: Session, user_in: UserCreate, role: Role = Role.user) -> User:
    hashed = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def admin_invite_user(db: Session, user_in: UserCreate) -> User:
    return create_user(db, user_in, role=Role.admin)

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).get(user_id)

def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update_user(
    db: Session,
    user_id: int,
    user_in: UserUpdate,
    role: Role | None = None
) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None

    data = user_in.dict(exclude_unset=True)
    if data.get("password"):
        user.hashed_password = get_password_hash(data.pop("password"))
    if data.get("email"):
        user.email = data["email"]
    if data.get("full_name") is not None:
        user.full_name = data["full_name"]
    if role:
        user.role = role

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
def generate_password_reset(db: Session, email: str) -> dict | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    token = create_password_reset_token(user.email)
    reset_link = f"{Settings.FRONTEND_URL}/reset-password?token={token}"
    return {
        "email": user.email,
        "full_name": user.full_name,
        "reset_link": reset_link
    }

def reset_user_password(db: Session, token: str, new_password: str):

    # 1. Verify token and extract email
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired reset token")

    # 2. Fetch the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    # 3. Hash & update
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return user
def admin_password_reset(db: Session, user_id: int) -> dict:
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    token = create_password_reset_token(user.email)
    reset_link = f"{Settings.FRONTEND_URL}/reset-password?token={token}"

    return {
        "email": user.email,
        "full_name": user.full_name,
        "reset_link": reset_link
    }
