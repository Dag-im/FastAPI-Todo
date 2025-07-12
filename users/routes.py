from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session

from core.database import get_db
from users.schema import (
    UserCreate,
    UserItem,
    UserListResponse,
    UserUpdate,
    ResetPasswordIn
)
from users.services import (
    create_user,
    list_users,
    get_user,
    admin_invite_user,
    update_user,
    delete_user,
    reset_user_password,
    generate_password_reset,
    admin_password_reset
)
from auth.services import get_current_user, get_current_admin
from users.models import Role, User
from utils.email import send_email
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["users"])

# ─────── Public / Self-Service ───────

@router.post(
    "/",
    response_model=UserItem,
    status_code=status.HTTP_201_CREATED,
    summary="Register yourself as a new user"
)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, user_in, role=Role.user)
    return user

@router.get(
    "/me",
    response_model=UserItem,
    summary="Get your own profile"
)
def read_own_profile(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user

# ─────── Admin‑Only ───────

@router.get(
    "/",
    response_model=UserListResponse,
    summary="[Admin] List users",
)
def admin_list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db),
    _: UserItem = Depends(get_current_admin)
):
    users = list_users(db, skip=skip, limit=limit)
    return {"users": users}

@router.get(
    "/{user_id}",
    response_model=UserItem,
    summary="[Admin] Get user by ID"
)
def admin_get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: UserItem = Depends(get_current_admin)
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "/invite",
    response_model=UserItem,
    summary="[Admin] Invite a new user (create an admin user)"
)
def invite_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    _: UserItem = Depends(get_current_admin)
):
    if db.query(User).filter(User.email == user_in.email).first():
      raise HTTPException(status_code=400, detail="Email already registered")
    admin_user = admin_invite_user(db, user_in)
    return admin_user

@router.patch(
    "/{user_id}",
    response_model=UserItem,
    summary="[Admin] Update user fields / role"
)
def admin_update_user(
    user_id: int,
    user_in: UserUpdate,
    role: Role | None = None,
    db: Session = Depends(get_db),
    _: UserItem = Depends(get_current_admin)
):
    updated = update_user(db, user_id, user_in, role=role)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[Admin] Delete a user"
)
def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: UserItem = Depends(get_current_admin)
):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return

@router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Request a password reset link via email"
)
def forgot_password(
    email: EmailStr,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    reset_data = generate_password_reset(db, email)
    if reset_data:
        # Compose the HTML body
        html = f"""
        <p>Hello {reset_data['full_name'] or reset_data['email']},</p>
        <p>You requested a password reset. Click the link below to set a new password:</p>
        <p><a href="{reset_data['reset_link']}">Reset your password</a></p>
        <p>This link expires in 15 minutes.</p>
        """
        # Schedule the email send in background
        background_tasks.add_task(
            send_email,
            reset_data["email"],
            "Reset your password",
            html
        )

    # Always return success response
    return {"msg": "If that email exists, a reset link has been sent."}

@router.post(
    "/reset-password",
    response_model=dict,
    summary="Reset your password using a token"
)
def reset_password(
    data: ResetPasswordIn,
    db: Session = Depends(get_db)
):
    # Service will raise HTTPException on invalid token or missing user
    reset_user_password(db, data.token, data.new_password)
    return {"msg": "Password has been reset successfully."}

@router.post(
    "/{user_id}/reset-password",
    status_code=status.HTTP_202_ACCEPTED,
    summary="[Admin] Trigger password‑reset email for a user"
)
def admin_reset_password(
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: UserItem = Depends(get_current_admin)
):
    reset_data = admin_password_reset(db, user_id)

    html = f"""
    <p>Hello {reset_data['full_name'] or reset_data['email']},</p>
    <p>An administrator has requested a password reset for your account.
    Click the link below to choose a new password:</p>
    <p><a href="{reset_data['reset_link']}">Reset your password</a></p>
    <p>This link expires in 15 minutes.</p>
    """

    background_tasks.add_task(
        send_email,
        reset_data["email"],
        "Your password reset request",
        html
    )

    return {"msg": "Password reset email sent if user exists."}
