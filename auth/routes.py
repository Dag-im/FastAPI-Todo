from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth.schema import Token
from auth.services import oauth2_scheme, get_current_user, login_user
from core.database import get_db
from users.schema import UserItem  # assuming this is your public user output schema

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    response = login_user(db, form_data)
    if isinstance(response, dict) and "status_code" in response:
        raise HTTPException(
            status_code=response["status_code"],
            detail=response["detail"]
        )
    return response

@router.get("/users/me", response_model=UserItem)
def read_users_me(
    current_user = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return current_user
