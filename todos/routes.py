from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from . import schema, services
from auth.services import get_current_user
from users.schema import UserItem

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=schema.TodoListResponse, status_code=status.HTTP_200_OK)
def get_todos(
    db: Session = Depends(get_db),
    current_user: UserItem = Depends(get_current_user)
):
    try:
        todos = services.get_todos(db, user_id=current_user.id)
        if not todos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No todos found."
            )
        return {"todos": todos}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{todo_id}", response_model=schema.TodoItem, status_code=status.HTTP_200_OK)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserItem = Depends(get_current_user)
):
    try:
        todo = services.get_todo(db, todo_id, user_id=current_user.id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found."
            )
        return todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/", response_model=schema.TodoItem, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schema.TodoCreate,
    db: Session = Depends(get_db),
    current_user: UserItem = Depends(get_current_user)
):
    try:
        new_todo = services.create_todo(db, todo, user_id=current_user.id)
        return new_todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{todo_id}", response_model=schema.TodoItem, status_code=status.HTTP_200_OK)
def update_todo(
    todo_id: int,
    todo: schema.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: UserItem = Depends(get_current_user)
):
    try:
        updated_todo = services.update_todo(db, todo_id, todo, user_id=current_user.id)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found."
            )
        return updated_todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserItem = Depends(get_current_user)
):
    try:
        deleted = services.delete_todo(db, todo_id, user_id=current_user.id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found."
            )
        return {"detail": "Todo deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
